# --- Force using venv's PySide6/Qt first ---
import os
from pathlib import Path
from importlib.util import find_spec

_spec = find_spec("PySide6")
if _spec and _spec.origin:
    _pyside_dir = Path(_spec.origin).parent
    # 讓 Windows loader 先從 venv 的 PySide6 目錄找 Qt6*.dll
    if hasattr(os, "add_dll_directory"):
        os.add_dll_directory(str(_pyside_dir))
    # 鎖定 Qt 平台外掛與外掛根目錄
    os.environ.setdefault("QT_QPA_PLATFORM", "windows")
    os.environ.setdefault("QT_QPA_PLATFORM_PLUGIN_PATH", str(_pyside_dir / "plugins" / "platforms"))
    os.environ.setdefault("QT_PLUGIN_PATH", str(_pyside_dir / "plugins"))
# --- End force block ---


import subprocess
import sys
import os
import json
import psutil
import time
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox,
    QTextEdit, QFrame, QTabWidget, QFileDialog, 
    QTableWidget, QTableWidgetItem, QHeaderView,
    QCheckBox, QAbstractItemView, QMessageBox, QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QColor
from datetime import datetime
import hfss_api

# --- Constants ---
MACHINES_FILE = "machines.json"
DEFAULT_MACHINES = [
    {"name": "ahmed", "cores": 16, "ram": 64},
    {"name": "bill", "cores": 32, "ram": 128},
    {"name": "catherine", "cores": 8, "ram": 32},
    {"name": "dennis", "cores": 64, "ram": 256}
]

class HfssWorker(QThread):
    """
    Worker thread to run HFSS API calls without freezing the GUI.
    """
    data_ready = Signal(object)  # Emits the extracted project data dictionary

    def __init__(self, version_path, project_path):
        super().__init__()
        self.version_path = version_path
        self.project_path = project_path

    def run(self):
        """Executes the HFSS data extraction."""
        project_data = hfss_api.get_project_data(self.version_path, self.project_path)
        self.data_ready.emit(project_data)

class SchedulerWorker(QThread):
    """
    Worker thread to run the scheduler without freezing the GUI.
    """
    log_message = Signal(str)
    update_cell = Signal(int, int, str)
    update_row_status = Signal(int, str)
    task_started = Signal(int)
    schedule_finished = Signal()

    def __init__(self, schedule_table, hfss_versions):
        super().__init__()
        self.schedule_table = schedule_table
        self.hfss_versions = hfss_versions
        self.is_running = True
        self.completed_rows = set()

    def run(self):
        """Executes scheduler tasks and monitors for new ones."""
        while self.is_running:
            next_task_row = -1
            # Find the first task that hasn't been completed yet
            for i in range(self.schedule_table.rowCount()):
                if i in self.completed_rows:
                    continue
                if self.schedule_table.item(i, 7) and self.schedule_table.item(i, 7).text() == "---":
                    next_task_row = i
                    break
            
            if next_task_row != -1:
                i = next_task_row
                self.task_started.emit(i)
                start_time = datetime.now()
                self.update_cell.emit(i, 6, start_time.strftime("%Y-%m-%d %H:%M:%S"))
                self.update_row_status.emit(i, "highlight")

                # --- Get Task Data ---
                version_key = self.schedule_table.item(i, 0).text()
                version_path = self.hfss_versions.get(version_key)
                full_project_path = self.schedule_table.item(i, 8).text()
                step1_machine_str = self.schedule_table.item(i, 9).text()
                design = self.schedule_table.item(i, 2).text()
                setup = self.schedule_table.item(i, 3).text()
                machines_list_for_cmd = self.schedule_table.item(i, 5).text()
                
                if not version_path:
                    self.log_message.emit(f"ERROR: HFSS version '{version_key}' path not found. Skipping task.")
                    self.update_row_status.emit(i, "error") # You might want a specific color for errors
                    self.completed_rows.add(i)
                    continue

                ansysedt_exe = os.path.join(version_path, "ansysedt.exe")
                
                # --- Step 1: Disable Sweeps and Run Locally ---
                self.log_message.emit(f"--- STEP 1: Disabling sweeps for {design}:{setup} ---")
                sweeps_disabled = hfss_api.set_sweeps_enabled(version_path, full_project_path, design, setup, enabled=False)
                
                if sweeps_disabled:
                    self.log_message.emit("Sweeps disabled successfully.")

                    local_run_command = (
                        f'"{ansysedt_exe}" -ng -distributed -auto '
                        f'-machinelist list="{step1_machine_str}" -batchsolve '
                        f'"{design}:Nominal:{setup}" "{full_project_path}"'
                    )
                    self.log_message.emit(f"Executing: {local_run_command}")
                    process = subprocess.run(local_run_command, shell=True, capture_output=True, text=True)
                    if process.stdout:
                        self.log_message.emit(f"STDOUT:\n{process.stdout}")
                    if process.stderr:
                        self.log_message.emit(f"STDERR:\n{process.stderr}")
                else:
                    self.log_message.emit("ERROR: Failed to disable sweeps. Skipping local run.")
                    self.update_row_status.emit(i, "error")
                    self.completed_rows.add(i)
                    continue # Skip to next task

                if not self.is_running:
                    self.log_message.emit("Task execution was stopped after local run.")
                    break

                # --- Step 2: Enable Sweeps and Run Distributed ---
                self.log_message.emit(f"--- STEP 2: Enabling sweeps for {design}:{setup} ---")
                sweeps_enabled = hfss_api.set_sweeps_enabled(version_path, full_project_path, design, setup, enabled=True)

                if sweeps_enabled:
                    self.log_message.emit("Sweeps enabled successfully.")
                    distributed_run_command = (
                        f'"{ansysedt_exe}" -ng -distributed -auto '
                        f'-machinelist list="{machines_list_for_cmd}" -batchsolve '
                        f'"{design}:Nominal:{setup}" "{full_project_path}"'
                    )
                    self.log_message.emit(f"Executing: {distributed_run_command}")
                    process = subprocess.run(distributed_run_command, shell=True, capture_output=True, text=True)
                    if process.stdout:
                        self.log_message.emit(f"STDOUT:\n{process.stdout}")
                    if process.stderr:
                        self.log_message.emit(f"STDERR:\n{process.stderr}")
                else:
                    self.log_message.emit("ERROR: Failed to re-enable sweeps. Skipping distributed run.")
                    self.update_row_status.emit(i, "error")
                    self.completed_rows.add(i)
                    continue

                # --- Finalize Task ---
                end_time = datetime.now()
                duration = end_time - start_time
                total_seconds = duration.total_seconds()
                h, rem = divmod(total_seconds, 3600)
                m, s = divmod(rem, 60)
                duration_str = f"{int(h):02}:{int(m):02}:{int(s):02}"

                self.update_cell.emit(i, 7, duration_str)
                self.update_row_status.emit(i, "finished")
                self.task_started.emit(-1) # Reset current task
                self.completed_rows.add(i)
            else:
                self.log_message.emit("No pending tasks. Monitoring for new tasks every 10 seconds...")
                for _ in range(10):
                    if not self.is_running:
                        break
                    time.sleep(1)
        
        self.schedule_finished.emit()

    def stop(self):
        self.is_running = False

class MockupUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HFSS 自動化批次求解工具")
        self.setGeometry(100, 100, 900, 700)
        self.project_data = {}
        self.hfss_versions = {}
        self.machines = []
        self.full_machine_list = []
        self.scheduler_worker = None
        self.current_task_row = -1
        self.step1_machine_group = QButtonGroup()
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        self.tabs = QTabWidget()
        self.task_tab = QWidget()
        self.scheduler_tab = QWidget()
        self.machine_tab = QWidget()
        
        self.tabs.addTab(self.task_tab, "任務")
        self.tabs.addTab(self.scheduler_tab, "排程器")
        self.tabs.addTab(self.machine_tab, "機器列表")
        self.help_tab = QWidget()
        self.tabs.addTab(self.help_tab, "說明")
        
        self._create_task_tab()
        self._create_scheduler_tab()
        self._create_machine_tab()
        self._create_help_tab()

        main_layout.addWidget(self.tabs)

        self._connect_signals()
        self._detect_hfss_versions()

        self.load_machines()
        self.log_message(self.task_log, "應用程式啟動。請選擇 HFSS 版本並瀏覽專案檔。")
        self._update_add_to_schedule_button_state()

    def _update_add_to_schedule_button_state(self):
        is_setup_selected = bool(self.setup_combo.currentText())
        
        is_step2_machine_selected = False
        for row in range(self.task_machine_table.rowCount()):
            checkbox_widget = self.task_machine_table.cellWidget(row, 1)
            if checkbox_widget:
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    is_step2_machine_selected = True
                    break
        
        self.add_to_schedule_button.setEnabled(is_setup_selected and is_step2_machine_selected)

    def _style_button(self, button, color):
        """Applies a consistent style to a button."""
        style = {
            "green": "background-color: #4CAF50; color: white;",
            "red": "background-color: #f44336; color: white;",
            "blue": "background-color: #2196F3; color: white;"
        }
        
        disabled_style = "background-color: #CCCCCC; color: #888888;"
        pressed_style = "background-color: #1E88E5;"

        if color == 'green':
            disabled_style = "background-color: #A5D6A7; color: #616161;"
            pressed_style = "background-color: #45a049;"
        elif color == 'red':
            pressed_style = "background-color: #da190b;"

        base_style = f"""
            QPushButton {{
                {style.get(color, style['blue'])}
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
            QPushButton:pressed {{
                {pressed_style}
            }}
            QPushButton:disabled {{
                {disabled_style}
            }}
        """
        button.setStyleSheet(base_style)
        button.setMinimumWidth(120)
    def _create_task_tab(self):
        layout = QVBoxLayout(self.task_tab)
        # --- HFSS Version Selection ---
        version_layout = QHBoxLayout()
        version_layout.addWidget(QLabel("HFSS 版本:"))
        self.task_hfss_version_combo = QComboBox()
        version_layout.addWidget(self.task_hfss_version_combo)
        version_layout.addStretch()
        layout.addLayout(version_layout)
        
        project_path_layout = QHBoxLayout()
        project_path_label = QLabel("專案路徑:")
        self.project_path_line_edit = QLineEdit()
        self.browse_button = QPushButton("瀏覽...")
        self._style_button(self.browse_button, "blue")
        project_path_layout.addWidget(project_path_label)
        project_path_layout.addWidget(self.project_path_line_edit)
        project_path_layout.addWidget(self.browse_button)
        layout.addLayout(project_path_layout)
        solver_and_machine_layout = QHBoxLayout()
        solver_settings_frame = QFrame()
        solver_settings_frame.setFrameShape(QFrame.StyledPanel)
        solver_settings_layout = QGridLayout(solver_settings_frame)
        
        solver_settings_layout.addWidget(QLabel("設計 (Design):"), 0, 0)
        self.design_combo = QComboBox()
        solver_settings_layout.addWidget(self.design_combo, 0, 1)
        solver_settings_layout.addWidget(QLabel("設定 (Setup):"), 1, 0)
        self.setup_combo = QComboBox()
        solver_settings_layout.addWidget(self.setup_combo, 1, 1)
        solver_settings_layout.addWidget(QLabel("掃描 (Sweeps):"), 2, 0)
        self.sweeps_text = QTextEdit()
        self.sweeps_text.setReadOnly(True)
        solver_settings_layout.addWidget(self.sweeps_text, 2, 1)
        solver_and_machine_layout.addWidget(solver_settings_frame, 1)
        machine_params_layout = QVBoxLayout()
        
        distributed_group = QFrame()
        distributed_group.setFrameShape(QFrame.StyledPanel)
        distributed_layout = QVBoxLayout(distributed_group)
        distributed_layout.addWidget(QLabel("<b>分散式設定</b>"), 0, Qt.AlignCenter)
        
        self.task_machine_table = QTableWidget()
        self.task_machine_table.setColumnCount(6)
        self.task_machine_table.setHorizontalHeaderLabels(["第一階段", "第二階段", "機器名稱", "可用核心", "使用核心", "RAM (%)"])
        header = self.task_machine_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        distributed_layout.addWidget(self.task_machine_table)
        
        machine_params_layout.addWidget(distributed_group)
        
        solver_and_machine_layout.addLayout(machine_params_layout, 2)
        layout.addLayout(solver_and_machine_layout)
        
        add_to_schedule_layout = QHBoxLayout()
        self.add_to_schedule_button = QPushButton("加入排程")
        self._style_button(self.add_to_schedule_button, "green")
        add_to_schedule_layout.addStretch()
        add_to_schedule_layout.addWidget(self.add_to_schedule_button)
        layout.addLayout(add_to_schedule_layout)
        self.task_log = QTextEdit()
        self.task_log.setReadOnly(True)
        layout.addWidget(QLabel("任務日誌:"))
        layout.addWidget(self.task_log, 1)
    def _create_scheduler_tab(self):
        layout = QVBoxLayout(self.scheduler_tab)
        
        self.schedule_table = QTableWidget()
        self.schedule_table.setColumnCount(10) # Added version and hidden path
        self.schedule_table.setHorizontalHeaderLabels([
            "HFSS 版本", "專案", "設計", "設定", "掃描", 
            "分散式機器", "開始執行時間", "所用時間", "Full Path", "Step 1 Machine"
        ])
        self.schedule_table.setColumnHidden(8, True) # Hide the full path column
        self.schedule_table.setColumnHidden(9, True) # Hide the step 1 machine column
        self.schedule_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.schedule_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.schedule_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.schedule_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        layout.addWidget(QLabel("專案排程:"))
        layout.addWidget(self.schedule_table)
        
        schedule_buttons_layout = QHBoxLayout()
        self.toggle_schedule_button = QPushButton("啟動排程")
        self.remove_from_schedule_button = QPushButton("從排程中移除")
        self.move_up_button = QPushButton("上移")
        self.move_down_button = QPushButton("下移")
        
        self._style_button(self.toggle_schedule_button, "green")
        self._style_button(self.remove_from_schedule_button, "red")
        self._style_button(self.move_up_button, "blue")
        self._style_button(self.move_down_button, "blue")

        schedule_buttons_layout.addWidget(self.remove_from_schedule_button)
        schedule_buttons_layout.addWidget(self.move_up_button)
        schedule_buttons_layout.addWidget(self.move_down_button)
        schedule_buttons_layout.addStretch()
        schedule_buttons_layout.addWidget(self.toggle_schedule_button)
        layout.addLayout(schedule_buttons_layout)
        
        self.scheduler_log = QTextEdit()
        self.scheduler_log.setReadOnly(True)
        layout.addWidget(QLabel("排程日誌:"))
        layout.addWidget(self.scheduler_log, 1)
    def _create_machine_tab(self):
        layout = QVBoxLayout(self.machine_tab)
        layout.addWidget(QLabel("<b>分散式計算機器列表管理</b>"))
        self.machine_table = QTableWidget()
        self.machine_table.setColumnCount(3)
        self.machine_table.setHorizontalHeaderLabels(["機器名稱", "核心數", "RAM (GB)"])
        header = self.machine_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.machine_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.machine_table)
        input_frame = QFrame()
        input_frame.setFrameShape(QFrame.StyledPanel)
        input_layout = QGridLayout(input_frame)
        input_layout.addWidget(QLabel("名稱:"), 0, 0)
        self.new_machine_name = QLineEdit()
        input_layout.addWidget(self.new_machine_name, 0, 1)
        input_layout.addWidget(QLabel("核心數:"), 1, 0)
        self.new_machine_cores = QLineEdit()
        input_layout.addWidget(self.new_machine_cores, 1, 1)
        input_layout.addWidget(QLabel("RAM (GB):"), 2, 0)
        self.new_machine_ram = QLineEdit()
        input_layout.addWidget(self.new_machine_ram, 2, 1)
        
        self.add_machine_button = QPushButton("新增")
        self.update_machine_button = QPushButton("更新選定")
        self.delete_machine_button = QPushButton("刪除選定")
        self._style_button(self.add_machine_button, "green")
        self._style_button(self.update_machine_button, "blue")
        self._style_button(self.delete_machine_button, "red")
        machine_button_layout = QHBoxLayout()
        machine_button_layout.addWidget(self.add_machine_button)
        machine_button_layout.addWidget(self.update_machine_button)
        machine_button_layout.addWidget(self.delete_machine_button)
        machine_button_layout.addStretch()
        
        input_layout.addLayout(machine_button_layout, 3, 0, 1, 2)
        layout.addWidget(input_frame)
        self.machine_log = QTextEdit()
        self.machine_log.setReadOnly(True)
        layout.addWidget(QLabel("機器管理日誌:"))
        layout.addWidget(self.machine_log, 1)

    def _create_help_tab(self):
        """Creates the UI for the Help tab."""
        layout = QVBoxLayout(self.help_tab)
        help_text_edit = QTextEdit()
        help_text_edit.setReadOnly(True)
        
        help_html = """
        <html>
        <head>
            <style>
                body { font-family: "Microsoft JhengHei", sans-serif; font-size: 14px; }
                h3 { color: #00529B; }
                h4 { color: #2E8B57; }
                p, li { line-height: 1.6; }
                hr { border: 1px solid #ccc; }
            </style>
        </head>
        <body>
            <h3>歡迎使用 HFSS 自動化批次求解工具</h3>
            <p>本工具旨在簡化並自動化 ANSYS HFSS 的模擬流程，特別是針對需要兩階段求解的複雜任務。</p>
            <hr>

            <h4>1. 任務 (Task) 頁籤</h4>
            <p>此頁籤用於設定單一的求解任務。</p>
            <ul>
                <li><b>HFSS 版本:</b> 從下拉選單中選擇您已安裝的 ANSYS EM 版本。程式會自動偵測您電腦中的環境變數。</li>
                <li><b>專案路徑:</b> 點擊 "瀏覽..." 按鈕，選擇您的 <code>.aedt</code> 專案檔。選擇後，程式會自動解析專案內的設計 (Design)、設定 (Setup) 與掃描 (Sweeps)。</li>
                <li><b>設計 (Design) / 設定 (Setup):</b> 根據解析出的專案內容，選擇您要執行的設計與設定。</li>
                <li><b>掃描 (Sweeps):</b> 此處會顯示所選設定中包含的掃描分析，僅供參考。</li>
                <li><b>分散式設定:</b>
                    <ul>
                        <li>此表格列出了可用於分散式計算的機器 (包含本機 localhost)。</li>
                        <li>勾選 "選用" 來決定哪些機器要參與 <b>第二階段 (啟用 Sweep)</b> 的分散式求解。</li>
                        <li>您可以修改每台機器要使用的 "使用核心" 數量與 "RAM (%)"。</li>
                    </ul>
                </li>
                <li><b>加入排程:</b> 設定完成後，點擊此按鈕將任務新增到 "排程器" 頁籤中。</li>
            </ul>
            <hr>

            <h4>2. 排程器 (Scheduler) 頁籤</h4>
            <p>此頁籤管理所有已新增的任務佇列。</p>
            <ul>
                <li><b>任務列表:</b> 顯示所有等待執行、正在執行或已完成的任務。</li>
                <li><b>從排程中移除:</b> 選擇一個或多個任務，點擊此按鈕將其從佇列中刪除 (僅限未開始的任務)。</li>
                <li><b>上移 / 下移:</b> 調整所選任務在佇列中的執行順序。</li>
                <li><b>啟動排程 / 停止排程:</b>
                    <ul>
                        <li>點擊 "啟動排程" 開始依序執行列表中的任務。</li>
                        <li>執行開始後，按鈕會變為 "停止排程"。點擊可手動中斷整個排程。</li>
                    </ul>
                </li>
            </ul>
            <p><b>執行流程:</b><br>
            當排程啟動時，每個任務都會嚴格遵循以下兩步驟：</p>
            <ol>
                <li><b>第一階段 (停用 Sweep):</b> 程式會自動修改專案檔，<b>停用</b>所有掃描分析，然後僅使用 <b>localhost</b> 進行本地求解。</li>
                <li><b>第二階段 (啟用 Sweep):</b> 第一階段完成後，程式會再次修改專案檔，<b>重新啟用</b>所有掃描分析，然後使用您在 "任務" 頁籤中選定的所有機器進行分散式求解。</li>
            </ol>
            <hr>

            <h4>3. 機器列表 (Machine List) 頁籤</h4>
            <p>此頁籤用於管理遠端的計算機器資源。</p>
            <ul>
                <li><b>新增:</b> 在下方的輸入框中填寫機器的名稱、核心數與 RAM (GB)，然後點擊 "新增"。</li>
                <li><b>更新選定:</b> 在列表中選擇一台機器，下方的輸入框會自動填入其資訊。修改後，點擊此按鈕進行更新。</li>
                <li><b>刪除選定:</b> 選擇一台機器，點擊此按鈕將其刪除。</li>
                <li><b>注意:</b> <code>localhost</code> 為本機，其資訊由程式自動偵測，無法修改或刪除。</li>
            </ul>
        </body>
        </html>
        """
        help_text_edit.setHtml(help_html)
        layout.addWidget(help_text_edit)

    def _connect_signals(self):
        self.browse_button.clicked.connect(self.browse_project)
        self.design_combo.currentIndexChanged.connect(self.update_setups)
        self.setup_combo.currentIndexChanged.connect(self.update_sweeps)
        self.setup_combo.currentIndexChanged.connect(self._update_add_to_schedule_button_state)
        self.add_to_schedule_button.clicked.connect(self.add_to_schedule)
        self.toggle_schedule_button.clicked.connect(self.toggle_schedule)
        self.remove_from_schedule_button.clicked.connect(self.remove_from_schedule)
        self.move_up_button.clicked.connect(self.move_schedule_item_up)
        self.move_down_button.clicked.connect(self.move_schedule_item_down)
        self.add_machine_button.clicked.connect(self.add_machine)
        self.update_machine_button.clicked.connect(self.update_machine)
        self.delete_machine_button.clicked.connect(self.delete_machine)
        self.machine_table.itemSelectionChanged.connect(self.on_machine_select)
        self.task_machine_table.itemChanged.connect(self.validate_task_machine_input)
    def load_machines(self):
        try:
            cpu_cores = psutil.cpu_count(logical=True)
            ram_gb = round(psutil.virtual_memory().total / (1024**3))
            localhost_info = {"name": "localhost", "cores": cpu_cores, "ram": ram_gb}
        except Exception as e:
            localhost_info = {"name": "localhost", "cores": 0, "ram": 0}
            self.log_message(self.machine_log, f"無法偵測本機硬體: {e}")
        try:
            if os.path.exists(MACHINES_FILE):
                with open(MACHINES_FILE, 'r', encoding='utf-8') as f:
                    self.machines = json.load(f)
            else:
                self.machines = DEFAULT_MACHINES[:]
                self.save_machines()
        except (IOError, json.JSONDecodeError) as e:
            self.machines = DEFAULT_MACHINES[:]
            self.log_message(self.machine_log, f"讀取檔案錯誤: {e}。使用預設列表。")
        
        self.full_machine_list = [localhost_info] + self.machines
        self.update_machine_lists()
    def save_machines(self):
        try:
            with open(MACHINES_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.machines, f, indent=4, ensure_ascii=False)
            self.log_message(self.machine_log, f"機器列表已儲存至 {MACHINES_FILE}。")
        except IOError as e:
            self.log_message(self.machine_log, f"儲存檔案錯誤: {e}。")
    def log_message(self, log_widget, message):
        log_widget.append(message)
    def _detect_hfss_versions(self):
        self.hfss_versions = hfss_api.find_ansys_versions()
        if not self.hfss_versions:
            self.log_message(self.task_log, "警告: 未偵測到任何 ANSYS EM 版本環境變數。")
            self.task_hfss_version_combo.addItem("N/A")
            self.browse_button.setEnabled(False)
        else:
            # Sort versions from latest to oldest (e.g., v251, v242, v232)
            sorted_versions = sorted(
                self.hfss_versions.keys(),
                key=lambda v: int(v.lstrip('v')),
                reverse=True
            )
            self.task_hfss_version_combo.addItems(sorted_versions)
    def browse_project(self):
        aedt_path, _ = QFileDialog.getOpenFileName(self, "選擇專案檔", "", "Ansys Electronics Desktop Files (*.aedt)")
        if not aedt_path:
            return
        selected_version_key = self.task_hfss_version_combo.currentText()
        if selected_version_key not in self.hfss_versions:
            self.log_message(self.task_log, "錯誤: 無效的 HFSS 版本選擇。")
            return
        self.project_path_line_edit.setText(aedt_path)
        self.log_message(self.task_log, f"已選擇專案: {aedt_path}")
        self.log_message(self.task_log, "正在解析專案，請稍候...")
        # Disable UI during processing
        self.tabs.setEnabled(False)
        version_path = self.hfss_versions[selected_version_key]
        self.worker = HfssWorker(version_path=version_path, project_path=aedt_path)
        self.worker.data_ready.connect(self._on_hfss_data_loaded)
        self.worker.start()
    def _on_hfss_data_loaded(self, data):
        self.tabs.setEnabled(True)  # Re-enable UI
        if data is None:
            self.log_message(self.task_log, "錯誤: 無法從專案中解析資料。請檢查日誌。" )
            self.project_data = {}
        else:
            self.log_message(self.task_log, "專案解析成功。" )
            self.project_data = data
        
        self.update_designs()
        self._update_add_to_schedule_button_state()
    def update_designs(self):
        self.design_combo.clear()
        self.setup_combo.clear()
        self.sweeps_text.clear()
        if self.project_data:
            self.design_combo.addItems(self.project_data.keys())
    def update_setups(self):
        self.setup_combo.clear()
        self.sweeps_text.clear()
        current_design = self.design_combo.currentText()
        if current_design in self.project_data:
            self.setup_combo.addItems(self.project_data[current_design].keys())
    def update_sweeps(self):
        self.sweeps_text.clear()
        current_design = self.design_combo.currentText()
        current_setup = self.setup_combo.currentText()
        if current_design and current_setup:
            sweeps = self.project_data.get(current_design, {}).get(current_setup, [])
            self.sweeps_text.setText("\n".join(sweeps))
    def add_to_schedule(self):
        aedt_path = self.project_path_line_edit.text()
        if not aedt_path:
            self.log_message(self.task_log, "錯誤: 請先選擇一個專案。" )
            return
        
        hfss_version = self.task_hfss_version_combo.currentText()
        design = self.design_combo.currentText()
        setup = self.setup_combo.currentText()
        if not all([hfss_version, design, setup]) or hfss_version == "N/A":
            self.log_message(self.task_log, "錯誤: 請選擇有效的 HFSS 版本、設計與設定。" )
            return
        sweeps = self.sweeps_text.toPlainText().split('\n')
        
        distributed_tasks = []
        for row in range(self.task_machine_table.rowCount()):
            checkbox = self.task_machine_table.cellWidget(row, 1).findChild(QCheckBox)
            if checkbox and checkbox.isChecked():
                name = self.task_machine_table.item(row, 2).text()
                cores = self.task_machine_table.item(row, 4).text()
                ram = self.task_machine_table.item(row, 5).text()
                # Correct format: machine_name:-1:cores:ram%
                distributed_tasks.append(f"{name}:-1:{cores}:{ram}%")
        
        if not distributed_tasks:
            self.log_message(self.task_log, "錯誤: 請至少為第二階段選擇一台分散式計算機器。" )
            return

        step1_machine_button = self.step1_machine_group.checkedButton()
        if not step1_machine_button:
            self.log_message(self.task_log, "錯誤: 請為第一階段選擇一台機器。")
            return
        step1_machine_row = -1
        for i in range(self.task_machine_table.rowCount()):
            radio_button = self.task_machine_table.cellWidget(i, 0).findChild(QRadioButton)
            if radio_button == step1_machine_button:
                step1_machine_row = i
                break
        
        step1_name = self.task_machine_table.item(step1_machine_row, 2).text()
        step1_cores = self.task_machine_table.item(step1_machine_row, 4).text()
        step1_ram = self.task_machine_table.item(step1_machine_row, 5).text()
        step1_machine_str = f"{step1_name}:-1:{step1_cores}:{step1_ram}%"


        row_position = self.schedule_table.rowCount()
        self.schedule_table.insertRow(row_position)

        self.schedule_table.setItem(row_position, 0, QTableWidgetItem(hfss_version))
        self.schedule_table.setItem(row_position, 1, QTableWidgetItem(os.path.basename(aedt_path)))
        self.schedule_table.setItem(row_position, 2, QTableWidgetItem(design))
        self.schedule_table.setItem(row_position, 3, QTableWidgetItem(setup))
        self.schedule_table.setItem(row_position, 4, QTableWidgetItem(", ".join(sweeps)))
        self.schedule_table.setItem(row_position, 5, QTableWidgetItem(",".join(distributed_tasks)))
        self.schedule_table.setItem(row_position, 6, QTableWidgetItem("---")) # Start Time
        self.schedule_table.setItem(row_position, 7, QTableWidgetItem("---")) # Elapsed Time
        self.schedule_table.setItem(row_position, 8, QTableWidgetItem(aedt_path)) # Hidden full path
        self.schedule_table.setItem(row_position, 9, QTableWidgetItem(step1_machine_str)) # Hidden step 1 machine

        success_message = f"已將任務 '{os.path.basename(aedt_path)}' (版本: {hfss_version}) 加入排程。"
        self.log_message(self.scheduler_log, success_message)
        self.log_message(self.task_log, success_message)
    def remove_from_schedule(self):
        selected_rows = sorted([index.row() for index in self.schedule_table.selectionModel().selectedRows()], reverse=True)
        if not selected_rows:
            self.log_message(self.scheduler_log, "請先選擇要從排程中移除的任務。")
            return
        
        for row in selected_rows:
            if self.scheduler_worker and row == self.current_task_row:
                self.log_message(self.scheduler_log, f"錯誤: 無法移除正在執行的任務。")
                continue
            
            if self.schedule_table.item(row, 7).text() != "---":
                self.log_message(self.scheduler_log, f"錯誤: 無法移除已完成的任務。")
                continue
            project_name = self.schedule_table.item(row, 1).text()
            self.schedule_table.removeRow(row)
            self.log_message(self.scheduler_log, f"已從排程中移除: {project_name}")
    def move_schedule_item_up(self):
        row = self.schedule_table.currentRow()
        if row < 0: return
        if self.scheduler_worker and (row == self.current_task_row or (row - 1) == self.current_task_row):
            self.log_message(self.scheduler_log, "錯誤: 無法移動正在執行或即將執行的任務。")
            return
        
        if self.schedule_table.item(row, 7).text() != "---":
            self.log_message(self.scheduler_log, "錯誤: 無法移動已完成的任務。")
            return
        if row > 0:
            self.schedule_table.insertRow(row + 1)
            for col in range(self.schedule_table.columnCount()):
                self.schedule_table.setItem(row + 1, col, self.schedule_table.takeItem(row - 1, col))
            self.schedule_table.removeRow(row - 1)
            self.schedule_table.selectRow(row - 1)
    def move_schedule_item_down(self):
        row = self.schedule_table.currentRow()
        if row < 0: return
        if self.scheduler_worker and (row == self.current_task_row or (row + 1) == self.current_task_row):
            self.log_message(self.scheduler_log, "錯誤: 無法移動正在執行或即將執行的任務。")
            return
            
        if self.schedule_table.item(row, 7).text() != "---":
            self.log_message(self.scheduler_log, "錯誤: 無法移動已完成的任務。")
            return
        if 0 <= row < self.schedule_table.rowCount() - 1:
            self.schedule_table.insertRow(row)
            for col in range(self.schedule_table.columnCount()):
                self.schedule_table.setItem(row, col, self.schedule_table.takeItem(row + 2, col))
            self.schedule_table.removeRow(row + 2)
            self.schedule_table.selectRow(row + 1)
            
    def toggle_schedule(self):
        if self.scheduler_worker and self.scheduler_worker.isRunning():
            self.stop_schedule()
        else:
            self.start_schedule()
    def start_schedule(self):
        if self.schedule_table.rowCount() == 0:
            self.log_message(self.scheduler_log, "排程為空，無法啟動。" )
            return
        
        self.toggle_schedule_button.setText("停止排程")
        self._style_button(self.toggle_schedule_button, "red")
        
        self.log_message(self.scheduler_log, "--- 開始執行排程 ---")
        self.scheduler_worker = SchedulerWorker(self.schedule_table, self.hfss_versions)
        self.scheduler_worker.log_message.connect(lambda msg: self.log_message(self.scheduler_log, msg))
        self.scheduler_worker.update_cell.connect(self.update_schedule_cell)
        self.scheduler_worker.update_row_status.connect(self.update_schedule_row_status)
        self.scheduler_worker.task_started.connect(self.on_task_started)
        self.scheduler_worker.schedule_finished.connect(self.on_schedule_finished)
        self.scheduler_worker.start()
    def stop_schedule(self):
        if self.scheduler_worker:
            self.scheduler_worker.stop()
            self.log_message(self.scheduler_log, "--- 排程已手動停止 ---")
            # The on_schedule_finished will be called automatically when the thread finishes
            
    def on_schedule_finished(self):
        self.log_message(self.scheduler_log, "--- 排程執行完畢 ---")
        self.toggle_schedule_button.setText("啟動排程")
        self._style_button(self.toggle_schedule_button, "green")
        self.scheduler_worker = None
        self.current_task_row = -1
        # Reset row colors for non-finished tasks
        for i in range(self.schedule_table.rowCount()):
            if self.schedule_table.item(i, 7) and self.schedule_table.item(i, 7).text() == "---":
                for j in range(self.schedule_table.columnCount()):
                    if self.schedule_table.item(i, j):
                        self.schedule_table.item(i, j).setBackground(QColor("white"))
    def on_task_started(self, row):
        self.current_task_row = row
    def update_schedule_cell(self, row, col, text):
        self.schedule_table.setItem(row, col, QTableWidgetItem(text))
    def update_schedule_row_status(self, row, status):
        color = QColor("white")
        if status == "highlight":
            color = QColor("yellow")
        elif status == "finished":
            color = QColor("lightgreen")
        elif status == "error":
            color = QColor(255, 102, 102) # Light red
        
        for j in range(self.schedule_table.columnCount()):
            if self.schedule_table.item(row, j):
                self.schedule_table.item(row, j).setBackground(color)
    def add_machine(self):
        name = self.new_machine_name.text().strip()
        if name.lower() == "localhost":
            self.log_message(self.machine_log, "錯誤: 'localhost' 是保留名稱。" )
            return
        cores = self.new_machine_cores.text().strip()
        ram = self.new_machine_ram.text().strip()
        if not all([name, cores, ram]):
            self.log_message(self.machine_log, "錯誤: 所有欄位皆為必填。" )
            return
        if any(m['name'] == name for m in self.machines):
            self.log_message(self.machine_log, f"錯誤: 機器 '{name}' 已存在。" )
            return
        try:
            self.machines.append({"name": name, "cores": int(cores), "ram": int(ram)})
            self.save_machines()
            self.load_machines() # Reload to refresh full list
            self.new_machine_name.clear()
            self.new_machine_cores.clear()
            self.new_machine_ram.clear()
        except ValueError:
            self.log_message(self.machine_log, "錯誤: 核心數與 RAM 必須是整數。" )
    def update_machine(self):
        row = self.machine_table.currentRow()
        if row < 0: return
        if self.machine_table.item(row, 0).text() == "localhost":
            self.log_message(self.machine_log, "無法更新 localhost。" )
            return
        
        name = self.new_machine_name.text().strip()
        cores = self.new_machine_cores.text().strip()
        ram = self.new_machine_ram.text().strip()
        if not all([name, cores, ram]): return
        
        json_index = row - 1
        original_name = self.machines[json_index]['name']
        if name != original_name and any(m['name'] == name for m in self.machines):
            self.log_message(self.machine_log, f"錯誤: 名稱 '{name}' 已存在。" )
            return
        try:
            self.machines[json_index] = {"name": name, "cores": int(cores), "ram": int(ram)}
            self.save_machines()
            self.load_machines()
        except ValueError:
            self.log_message(self.machine_log, "錯誤: 核心數與 RAM 必須是整數。" )
    def delete_machine(self):
        row = self.machine_table.currentRow()
        if row < 0:
            self.log_message(self.machine_log, "請先選擇要刪除的機器。" )
            return
        machine_name = self.machine_table.item(row, 0).text()
        if machine_name == "localhost":
            self.log_message(self.machine_log, "錯誤：無法刪除 localhost。" )
            return
        reply = QMessageBox.question(self, '確認刪除',
                                     f"您確定要刪除機器 '{machine_name}' 嗎？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # The index in the `self.machines` list is `row - 1` because of localhost
            del self.machines[row - 1]
            self.save_machines()
            self.load_machines()  # Reload and refresh the UI
            self.log_message(self.machine_log, f"已成功刪除機器 '{machine_name}'。" )
        else:
            self.log_message(self.machine_log, "刪除操作已取消。" )
    def on_machine_select(self):
        row = self.machine_table.currentRow()
        if row < 0: return
        
        is_localhost = (self.machine_table.item(row, 0).text() == "localhost")
        self.update_machine_button.setEnabled(not is_localhost)
        self.delete_machine_button.setEnabled(not is_localhost)
        self.new_machine_name.setReadOnly(is_localhost)
        self.new_machine_cores.setReadOnly(is_localhost)
        self.new_machine_ram.setReadOnly(is_localhost)
        machine = self.full_machine_list[row]
        self.new_machine_name.setText(machine['name'])
        self.new_machine_cores.setText(str(machine['cores']))
        self.new_machine_ram.setText(str(machine['ram']))
    def update_machine_lists(self):
        self.machine_table.setRowCount(0)
        read_only_color = QColor(240, 240, 240)  # Light gray
        for m in self.full_machine_list:
            row = self.machine_table.rowCount()
            self.machine_table.insertRow(row)
            
            name_item = QTableWidgetItem(m['name'])
            cores_item = QTableWidgetItem(str(m['cores']))
            ram_item = QTableWidgetItem(str(m['ram']))
            
            cores_item.setTextAlignment(Qt.AlignCenter)
            ram_item.setTextAlignment(Qt.AlignCenter)
            
            if m['name'] == 'localhost':
                flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled
                name_item.setFlags(flags)
                cores_item.setFlags(flags)
                ram_item.setFlags(flags)
                # Apply read-only color
                name_item.setBackground(read_only_color)
                cores_item.setBackground(read_only_color)
                ram_item.setBackground(read_only_color)
            self.machine_table.setItem(row, 0, name_item)
            self.machine_table.setItem(row, 1, cores_item)
            self.machine_table.setItem(row, 2, ram_item)
        self.task_machine_table.setRowCount(0)
        # Clear button group before repopulating
        for button in self.step1_machine_group.buttons():
            self.step1_machine_group.removeButton(button)

        for m in self.full_machine_list:
            row = self.task_machine_table.rowCount()
            self.task_machine_table.insertRow(row)
            
            # --- Step 1 Radio Button ---
            radio_button_widget = QWidget()
            radio_button_layout = QHBoxLayout(radio_button_widget)
            radio_button = QRadioButton()
            radio_button_layout.addWidget(radio_button)
            radio_button_layout.setAlignment(Qt.AlignCenter)
            radio_button_layout.setContentsMargins(0,0,0,0)
            self.task_machine_table.setCellWidget(row, 0, radio_button_widget)
            self.step1_machine_group.addButton(radio_button)

            # --- Step 2 Checkbox ---
            chk_box_widget = QWidget()
            chk_box_layout = QHBoxLayout(chk_box_widget)
            chk_box = QCheckBox()
            chk_box.stateChanged.connect(self._update_add_to_schedule_button_state)
            chk_box_layout.addWidget(chk_box)
            chk_box_layout.setAlignment(Qt.AlignCenter)
            chk_box_layout.setContentsMargins(0,0,0,0)
            self.task_machine_table.setCellWidget(row, 1, chk_box_widget)
            
            if m['name'] == 'localhost':
                radio_button.setChecked(True)
                chk_box.setChecked(True)

            # --- Machine Details ---
            machine_name_item = QTableWidgetItem(m['name'])
            machine_name_item.setFlags(machine_name_item.flags() & ~Qt.ItemIsEditable)
            machine_name_item.setBackground(read_only_color)
            self.task_machine_table.setItem(row, 2, machine_name_item)
            
            cores_item = QTableWidgetItem(str(m['cores']))
            cores_item.setFlags(cores_item.flags() & ~Qt.ItemIsEditable)
            cores_item.setBackground(read_only_color)
            self.task_machine_table.setItem(row, 3, cores_item)
            
            self.task_machine_table.setItem(row, 4, QTableWidgetItem(str(m['cores'])))
            self.task_machine_table.setItem(row, 5, QTableWidgetItem("75"))
    def validate_task_machine_input(self, item):
        row = item.row()
        col = item.column()
        
        if col == 4: # "使用核心" column
            try:
                cores_wanted = int(item.text())
                max_cores = int(self.task_machine_table.item(row, 3).text())
                if not (1 <= cores_wanted <= max_cores):
                    item.setText(str(max_cores))
            except (ValueError, TypeError):
                item.setText(self.task_machine_table.item(row, 3).text() or "1")
        if col == 5: # "RAM (%)" column
            try:
                if not (1 <= int(item.text()) <= 99):
                    item.setText("75")
            except (ValueError, TypeError):
                item.setText("75")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MockupUI()
    window.show()
    sys.exit(app.exec())
