# Display Manager API

```{eval-rst}
.. automodule:: core.display
   :members:
   :undoc-members:
   :show-inheritance:
```

## DisplayManager

Handles output formatting and display in various formats.

### Methods

#### display_all(data, sections)
Display all collected data in formatted terminal output.

**Parameters:**
- `data` (Dict[str, Any]): Collected system data
- `sections` (List[str]): List of sections to display

#### output_json(data)
Output data in JSON format.

**Parameters:**
- `data` (Dict[str, Any]): Data to output as JSON

#### save_to_file(data, file_path, sections)
Save data to a file.

**Parameters:**
- `data` (Dict[str, Any]): Data to save
- `file_path` (str): Path to output file
- `sections` (List[str]): Sections being saved

#### run_live_monitor(collector, sections)
Run live monitoring mode.

**Parameters:**
- `collector`: System collector instance
- `sections` (List[str]): Sections to monitor

### Display Methods

#### _display_system_info(data)
Display system information in formatted tables.

#### _display_hardware_info(data)
Display hardware information with visual elements.

#### _display_network_info(data)
Display network information and statistics.

#### _display_process_info(data)
Display process information with usage bars.

#### _display_security_info(data)
Display security status and information.

#### _display_sensor_info(data)
Display sensor readings and temperatures.

#### _display_python_info(data)
Display Python environment information.
