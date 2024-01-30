# 5.4 Request Custom File Naming

- **Default Naming Convention:** by default, files retain the name given by the uploader.

- **Enabling Custom Naming:** activate the custom file naming option to apply a systematic naming structure to the files.


- **Creating a Naming Formula:**
  - The custom naming involves a combination of text and parametric elements.
  - Use a formula structure where:
    - You can type static text.
    - Insert parametric elements within double curly brackets (`{{ }}`).
  - Choose the parametric part from a dropdown menu.

### **Example:**
If the naming formula is `{{upload_date}} - {{request_title}} - {{original_file_name}}`, and a file is uploaded the 2024-01-01 with the name `invoice-248` to a request titled `invoices October 2023` , it will be named as **`2024-01-01 - invoices October 2023 - invoice-248`** in your cloud storage.


