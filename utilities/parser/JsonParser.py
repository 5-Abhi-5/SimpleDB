
'''
parse json strings into Python objects from scratch.
This is a basic implementation of a JSON parser that can handle numbers, strings, booleans, arrays, and objects.
'''
class JsonParser:
    
    ''' Initializes the JsonParser with a JSON string.'''
    def __init__(self):
        self.counter = 0
    
    
    '''
    Parses a JSON string and returns the corresponding Python object.
    Raises ValueError if the JSON string is invalid or contains extra data after the valid JSON.
    '''
    def parse_json(self,json):
        length = len(json)
        res = self.parse(json)
        self.skip_whitespace(json)
        if self.counter != length:
            # print(json[self.counter:])
            raise ValueError("Extra data after valid JSON")
        return res
    
    
    ''' 
    Parses the JSON string and determines the type of the JSON value (object, array, string, number, boolean, or null) to call the appropriate parsing method.
    Raises ValueError if the JSON string is empty or starts with an invalid character.
    '''
    def parse(self,json):
        length = len(json)
        self.skip_whitespace(json)
        if self.counter >= length:
            # raise ValueError("Empty JSON string")
            return
        
        if json[self.counter] == '{':
            return self.parse_object(json)
        elif json[self.counter] == '[':
            return self.parse_array(json)
        elif json[self.counter] == '"':
            return self.parse_string(json)
        elif json[self.counter] in '-0123456789':
            return self.parse_number(json)
        elif json.startswith('true', self.counter):
            self.counter += 4
            return True
        elif json.startswith('false', self.counter):
            self.counter += 5
            return False    
        else:
            raise ValueError("Invalid JSON format")
    
    
    '''
    Parses a number from the JSON string.
    Handles both integers and floating-point numbers.
    '''
    def parse_number(self,json):
        res = ""
        length = len(json)
        if self.counter < length and (json[self.counter] == '-' or json[self.counter].isdigit()):
            if json[self.counter] == '-':
                res += '-'
                self.counter += 1
            while(self.counter < length and json[self.counter].isdigit()):
                res += json[self.counter]
                self.counter += 1
            if self.counter < length and json[self.counter] == '.':
                res += '.'
                self.counter += 1
                while(self.counter < length and json[self.counter].isdigit()):
                    res += json[self.counter]
                    self.counter += 1
                return float(res)
            return int(res)
        else:
            raise ValueError("Invalid number format")
    
    
    ''' 
    Parses a string from the JSON string.
    Handles escape sequences and checks for unterminated strings.
    '''
    def parse_string(self,json):
        res=""
        length = len(json)
        if self.counter >= length or json[self.counter] != '"':
            raise ValueError("String must start with '\"'")
        self.counter += 1  
        escape_sequences = {
            '"': '"',
            '\\': '\\',
            '/': '/',
            'b': '\b',
            'f': '\f',
            'n': '\n',
            'r': '\r',
            't': '\t'
        }
        while(self.counter < length and json[self.counter] != '"'):
            if json[self.counter] == '\\':
                self.counter += 1
                if self.counter >= length:
                    raise ValueError("Unterminated escape sequence")
                if json[self.counter] in escape_sequences:
                    res += escape_sequences[json[self.counter]]
                else:
                    raise ValueError(f"Invalid escape sequence: \\{json[self.counter]}")
            else:
                res += json[self.counter]
            self.counter += 1
        if self.counter < length and json[self.counter] == '"': 
            self.counter += 1
        else: 
            raise ValueError("Unterminated string")
        if res == 'null':
            return None
        return res
    
    
    ''' 
    Parses an array from the JSON string.
    Handles nested arrays and checks for unterminated arrays.
    '''
    def parse_array(self,json):
        res = []
        length = len(json)
        if self.counter >= length or json[self.counter] != '[':
            raise ValueError("Array must start with '['")
        self.counter += 1  
        while self.counter < length and json[self.counter] != ']':
            self.skip_whitespace(json)
            if self.check_null(json):
                value = None
            else:
                value = self.parse(json)
            res.append(value)
            self.skip_whitespace(json)
            if self.counter < length and json[self.counter] == ',':
                self.counter += 1
            elif self.counter < length and json[self.counter] == ']':
                self.counter += 1
                break
            else:
                raise ValueError("Expected ',' or ']' in array")
        else:
            raise ValueError("Unterminated array")
        return res
    
    
    ''' 
    Parses an object from the JSON string.
    Handles nested objects and checks for unterminated objects.
    '''
    def parse_object(self,json):
        res = {}
        length = len(json)
        if self.counter >= length or json[self.counter] != '{':
            raise ValueError("Object must start with '{'")
        self.counter += 1
        self.skip_whitespace(json)
        while self.counter < length and json[self.counter] != '}':
            self.skip_whitespace(json)
            if self.counter >= length:
                raise ValueError("Unterminated object")
            if json[self.counter] == ',':
                self.counter += 1
                self.skip_whitespace(json)
                continue
            key = self.parse_string(json)
            self.skip_whitespace(json)
            if self.counter >= length or json[self.counter] != ':':
                raise ValueError("Expected ':' after key in object")
            self.counter += 1
            self.skip_whitespace(json)
            if self.check_null(json):
                value = None
            else:
                value = self.parse(json)
            res[key] = value
            self.skip_whitespace(json)
        if self.counter < length and json[self.counter] == '}':
            self.counter += 1
        else:
            raise ValueError("Unterminated object")
        return res
        
    
    ''' 
    Skips whitespace characters in the JSON string.
    Increments the counter until a non-whitespace character
    '''
    def skip_whitespace(self,json):
        length = len(json)
        while(self.counter<length and json[self.counter].isspace()):
            self.counter += 1
    
    
    ''' 
    Checks for a null value in the JSON string.
    If 'null' is found, increments the counter and returns True.
    '''
    def check_null(self,json):
        self.skip_whitespace(json)
        length = len(json)
        if self.counter < length and json[self.counter] == 'n':
            if json.startswith('null', self.counter):
                self.counter += 4
                return True
            else:
                raise ValueError("Invalid null value")
            return True
        return False
    
    
    def dump_data(self,data,db_name):
        with open(db_name, 'w') as file:
            if isinstance(data, dict):
                file.write("{\n")
                for key, value in data.items():
                    file.write(f'  "{key}": "{value}",\n')
                file.write("}\n")
            elif isinstance(data, list):
                file.write("[\n")
                for item in data:
                    file.write(f' "{item}",\n')
                file.write("]\n")
            elif isinstance(data, str):
                file.write(f'"{data}"\n')
            elif isinstance(data, (int, float, bool)):
                file.write(f'"{data}"\n')
            elif data is None:
                file.write("null\n")
            # elif isinstance(data, (dict, list)):
            #     self.dump_data(self,data,db_name)
            else:
                raise ValueError("Unsupported data type for dumping")
        
    
    def load_data(self, db_name):
        data={}
        with open(db_name, 'r') as file:
            content = file.read()
            # print("Content read from file:", content)
            data = self.parse_json(content)
        if not data:
            return {}
        return data
            
    

'''Debugging and testing the JsonParser class.'''
if __name__ == "__main__":
    json__string = input("Enter a JSON string: ")
    parser = JsonParser(json__string)
    try:
        parsed_json = parser.parse_json()
        print("Parsed JSON:", parsed_json)
    except ValueError as e:
        print("Error parsing JSON:", e)
    # Example usage:
    # json_string = '{"name": "John", "age": 30, "is_student": false, "courses": ["Math", "Science"], "address": {"city": "New York", "zip": "10001"}, "null_value": null}'
    