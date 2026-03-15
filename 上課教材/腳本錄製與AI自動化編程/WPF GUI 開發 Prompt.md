# AEDT XAML GUI Design Guideline for AI Agents

When developing WPF Graphical User Interfaces (GUIs) to run within Ansys Electronic Desktop (AEDT / HFSS) via IronPython, AI Agents must strictly adhere to the following architecture, constraints, and fixes.

## 1. Environment Characteristics
* **Runtime**: IronPython running embedded within the Ansys AEDT AppDomain.
* **Component Framework**: Windows Presentation Foundation (WPF).
* **Execution Flow**: IronPython scripts call `.NET` libraries. Variables and UI contexts can persist across multiple script executions unless explicitly managed.

## 2. XAML Layout constraints
* **Separation of Concerns**: Design your UI layout in a standalone `.xaml` file (e.g., `window.xaml`), isolating layout descriptors from logic.
* **Namespaces**: Ensure default WPF namespaces are included at the root XML tag:
  ```xml
  xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
  xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
  ```
* **Event Handlers**: Do not use inline `x:Class` or C# event mappings like `Click="OnClick"` inside the XAML file, because IronPython parses the layout dynamically, independent of a compiled code-behind. Bind events instead in the IronPython script (e.g., `self.submit_button.Click += self.on_submit_click`).

## 3. IronPython Backend Setup
* **Required References**: Always reference these mandatory libraries at the start of your Python script:
  ```python
  import clr
  clr.AddReference("PresentationFramework")
  clr.AddReference("PresentationCore")
  clr.AddReference("WindowsBase")
  ```
* **Loading XAML**: Use `XamlReader.Load` from a `FileStream`. Avoid `StreamReader` wrapped string readers since `FileStream` is cleanly disposed by `.Close()`.
  
  ```python
  from System.IO import FileStream, FileMode, FileAccess
  from System.Windows.Markup import XamlReader
  
  stream = FileStream(xaml_path, FileMode.Open, FileAccess.Read)
  self.window = XamlReader.Load(stream)
  stream.Close()
  ```
* **Element Retrieval**: Use `self.window.FindName("ElementName")` to retrieve interactable controls.

## 4. The Re-Run NullReferenceException Error (CRITICAL FIX)
When the user closes the WPF window, the internal WPF `Application` object shuts down by default. However, Ansys retains the static reference `Application.Current`. If the script is run a second time, `XamlReader.Load()` tries to load against an invalid, disposed Application context, throwing a `NullReferenceException`.

**Resolution Guidelines:**
* Always check if `Application.Current` exists before launching the Window.
* If a new `Application` instance needs to be created, override the `ShutdownMode` property to `ShutdownMode.OnExplicitShutdown`. This prevents the AppDomain from implicitly killing the layout mechanisms when the first GUI is closed.
* Always launch the UI using `self.window.ShowDialog()` to block execution threads properly until user interaction is complete. Do not use `app.Run(window)`.

### Standard Boilerplate Entry Point:
```python
if __name__ == '__main__':
    from System.Windows import Application, ShutdownMode
    
    # Ensure current WPF Application does not die on window close
    try:
        if Application.Current is None:
            app = Application()
            app.ShutdownMode = ShutdownMode.OnExplicitShutdown
    except:
        # Ignore exceptions if Ansys has strict isolation or app already exists
        pass
        
    wpf_app = WpfApp()
    wpf_app.window.ShowDialog()
```

## 5. Event Binding and Callbacks
* IronPython supports standard `+=` operator syntax for registering delegates.
* Signature requires `(self, sender, event)`. Do not forget the `event` parameter.
  ```python
  self.my_button.Click += self.on_button_click

  def on_button_click(self, sender, event):
      MessageBox.Show("Clicked!")
  ```

## 6. General Coding Tips 
* **Absolute Paths**: HFSS changes the working directory depending on the project. Always resolve UI `.xaml` files using absolute paths relative to `__file__`:
  ```python
  import os
  current_dir = os.path.dirname(os.path.abspath(__file__))
  xaml_path = os.path.join(current_dir, "window.xaml")
  ```
* **Null Fallbacks**: Add fallback conditions or try-except blocks when updating GUI text manually since users might perform unexpected interactions that return `None` objects in events.
