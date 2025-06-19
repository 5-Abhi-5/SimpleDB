
'''
parse json strings into Python objects from scratch.
This is a basic implementation of a JSON parser that can handle numbers, strings, booleans, arrays, and objects.
'''
class JsonParser:
    
    ''' Initializes the JsonParser with a JSON string.'''
    def __init__(self, json):
        self.json = json
        self.counter = 0
        self.length = len(json)
    
    
    '''
    Parses a JSON string and returns the corresponding Python object.
    Raises ValueError if the JSON string is invalid or contains extra data after the valid JSON.
    '''
    def parse_json(self):
        res = self.parse()
        self.skip_whitespace()
        if self.counter != self.length:
            raise ValueError("Extra data after valid JSON")
        return res
    
    
    ''' 
    Parses the JSON string and determines the type of the JSON value (object, array, string, number, boolean, or null) to call the appropriate parsing method.
    Raises ValueError if the JSON string is empty or starts with an invalid character.
    '''
    def parse(self):
        self.skip_whitespace()
        if self.counter >= self.length:
            raise ValueError("Empty JSON string")
        
        if self.json[self.counter] == '{':
            return self.parse_object()
        elif self.json[self.counter] == '[':
            return self.parse_array()
        elif self.json[self.counter] == '"':
            return self.parse_string()
        elif self.json[self.counter] in '-0123456789':
            return self.parse_number()
        elif self.json.startswith('true', self.counter):
            self.counter += 4
            return True
        elif self.json.startswith('false', self.counter):
            self.counter += 5
            return False    
        else:
            raise ValueError("Invalid JSON format")
    
    
    '''
    Parses a number from the JSON string.
    Handles both integers and floating-point numbers.
    '''
    def parse_number(self):
        res = ""
        if self.counter < self.length and (self.json[self.counter] == '-' or self.json[self.counter].isdigit()):
            if self.json[self.counter] == '-':
                res += '-'
                self.counter += 1
            while(self.counter < self.length and self.json[self.counter].isdigit()):
                res += self.json[self.counter]
                self.counter += 1
            if self.counter < self.length and self.json[self.counter] == '.':
                res += '.'
                self.counter += 1
                while(self.counter < self.length and self.json[self.counter].isdigit()):
                    res += self.json[self.counter]
                    self.counter += 1
                return float(res)
            return int(res)
        else:
            raise ValueError("Invalid number format")
    
    
    ''' 
    Parses a string from the JSON string.
    Handles escape sequences and checks for unterminated strings.
    '''
    def parse_string(self):
        res=""
        if self.counter >= self.length or self.json[self.counter] != '"':
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
        while(self.counter < self.length and self.json[self.counter] != '"'):
            if self.json[self.counter] == '\\':
                self.counter += 1
                if self.counter >= self.length:
                    raise ValueError("Unterminated escape sequence")
                if self.json[self.counter] in escape_sequences:
                    res += escape_sequences[self.json[self.counter]]
                else:
                    raise ValueError(f"Invalid escape sequence: \\{self.json[self.counter]}")
            else:
                res += self.json[self.counter]
            self.counter += 1
        if self.counter < self.length and self.json[self.counter] == '"': 
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
    def parse_array(self):
        res = []
        if self.counter >= self.length or self.json[self.counter] != '[':
            raise ValueError("Array must start with '['")
        self.counter += 1  
        while self.counter < self.length and self.json[self.counter] != ']':
            self.skip_whitespace()
            if self.check_null():
                value = None
            else:
                value = self.parse()
            res.append(value)
            self.skip_whitespace()
            if self.counter < self.length and self.json[self.counter] == ',':
                self.counter += 1
            elif self.counter < self.length and self.json[self.counter] == ']':
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
    def parse_object(self):
        res = {}
        if self.counter >= self.length or self.json[self.counter] != '{':
            raise ValueError("Object must start with '{'")
        self.counter += 1
        while self.counter < self.length and self.json[self.counter] != '}':
            self.skip_whitespace()
            if self.counter >= self.length:
                raise ValueError("Unterminated object")
            if self.json[self.counter] == ',':
                self.counter += 1
                continue
            key = self.parse_string()
            self.skip_whitespace()
            if self.counter >= self.length or self.json[self.counter] != ':':
                raise ValueError("Expected ':' after key in object")
            self.counter += 1
            self.skip_whitespace()
            if self.check_null():
                value = None
            else:
                value = self.parse()
            res[key] = value
            self.skip_whitespace()
        if self.counter < self.length and self.json[self.counter] == '}':
            self.counter += 1
        else:
            raise ValueError("Unterminated object")
        return res
        
    
    ''' 
    Skips whitespace characters in the JSON string.
    Increments the counter until a non-whitespace character
    '''
    def skip_whitespace(self):
        while(self.counter<self.length and self.json[self.counter].isspace()):
            self.counter += 1
    
    
    ''' 
    Checks for a null value in the JSON string.
    If 'null' is found, increments the counter and returns True.
    '''
    def check_null(self):
        self.skip_whitespace()
        if self.counter < self.length and self.json[self.counter] == 'n':
            if self.json.startswith('null', self.counter):
                self.counter += 4
                return True
            else:
                raise ValueError("Invalid null value")
            return True
        return False
    

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
    