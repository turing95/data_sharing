import re


def fill_template(template_str, variables):
    # Function to replace each placeholder with the corresponding variable
    def replace(match):
        # Extract the variable name from the match
        var_name = match.group(1)
        # Return the variable's value from the dictionary, or the original string if not found
        return variables.get(var_name, match.group(0))

    # Regular expression pattern for finding {{variable}} placeholders
    pattern = r'\{\{(\w+)\}\}'

    # Use re.sub() to replace each placeholder with its value
    filled_str = re.sub(pattern, replace, template_str)

    return filled_str
