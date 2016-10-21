'''
POdB: A purchase order management system for small businesses 
Copyright (C) 2016  Paulo S. V. N. Leal

This program is free software: you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later 
version.

This program is distributed in the hope that it will be useful, but WITHOUT 
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS 
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with 
this program. If not, see <http://www.gnu.org/licenses/>.

Contact: paulosvnleal@gmail.com
'''

from decimal import Decimal


def percentage_int_to_decimal(value):
    '''Convert an integer representation of a percentage to a decimal type.
    
    Percentages are stored as integers in the database and are converted using
    this function into Decimal types for use in the application. 
    
    The function divides the supplied integer by 100 and converts it to decimal.
    
    Args:
    :param value: The percentage value to convert to decimal. 
    :type value: Integer
    
    Returns:
    :return: The percentage value as a decimal.
    :rtype: Decimal
    
    Raises:
    :raises: AssertionError if value is not an integer.
    :raises: ValueError if value is outside the range 0 to 99, inclusive.
    '''
    assert type(value) == int
    if value < 0 or value > 99:
        raise ValueError(("Parameter out of range in call to "
                          "percentage_int_to_decimal. The valid "
                          "range is 0 to 99, inclusive. "
                          "The parameter value was {}.").format(str(value)))
    return Decimal(value) / Decimal("100.0")

def percentage_decimal_to_int(value):
    '''Convert a decimal representation of a percentage to an integer.
    
    Percentages are stored as Decimal types in the application, and are 
    converted using this function into integers for storage in the database. 
    
    The function rounds the supplied decimal to two decimal places, multiplies 
    the result by 100.0 and converts it to an integer.
    
    Args:
    :param value: The percentage value to convert to integer.
    :type value: Decimal
    
    Returns:
    :return: The percentage value as an integer.
    :rtype: Integer
    
    Raises:
    :raises: AssertionError if value is not a Decimal.
    :raises: ValueError if value is outside the range 0.0 to 0.99, inclusive.
    '''
    assert type(value) == Decimal
    if value < Decimal("0.0") or value > Decimal("0.99"):
        raise ValueError(("Parameter out of range in call to "
                          "percentage_decimal_to_int. The valid "
                          "range is 0.0 to 0.99, inclusive. "
                          "The parameter value was {}.").format(str(value)))
    # Round the value to two decimal places before converting to integer.
    quantized_value = value.quantize(Decimal("1.00"))
    return int(quantized_value * Decimal("100.0"))

def monetary_int_to_decimal(value, app_config):
    '''Convert an integer representation of a monetary quantity, e.g., a price, 
    to a decimal type.
    
    Monetary quantities are stored as integers in the database and are converted 
    using this function into Decimal types for use in the application. 
    
    The number of decimal places used by the currency is configurable. This 
    function divides the supplied integer by a factor corresponding to the 
    required number of decimal places, and converts the result to decimal.
    
    Args:
    :param value: The monetary value to convert to decimal. 
    :type value: Integer
    :param app_config: The application configuration in use.
    :type app_confg: appconfig.ConfigFile
    
    Returns:
    :return: The monetary value as a decimal.
    :rtype: Decimal
    
    Raises:
    :raises: AssertionError if value is not an integer.
    '''
    assert type(value) == int
    # Calculate the factor from the configured decimal places.
    decimal_places = int(app_config.locale.currency_decimal_places)
    factor = 10 ** decimal_places
    return Decimal(value) / Decimal(factor)

def monetary_decimal_to_int(value, app_config):
    '''Convert a decimal representation of a monetary quantity, e.g., a price 
    to an integer.
    
    Monetary quantities are stored as Decimal types in the application, and are 
    converted using this function into integers for storage in the database. 
    
    The number of decimal places used by the currency is configurable. This 
    function multiplies the supplied decimal by a factor corresponding to the 
    required number of decimal places, and converts the result to integer.
    
    Args:
    :param value: The monetary value to convert to integer.
    :type value: Decimal
    :param app_config: The application configuration in use.
    :type app_confg: appconfig.ConfigFile
    
    Returns:
    :return: The monetary value as an integer.
    :rtype: Integer
    
    Raises:
    :raises: AssertionError if value is not a Decimal.
    '''
    assert type(value) == Decimal
    # Calculate the factor from the configured decimal places.
    decimal_places = int(app_config.locale.currency_decimal_places)
    factor = 10 ** decimal_places
    # Round the value the correct number of decimal places before converting to 
    # integer.
    quantize_spec_list = ["1."]
    for d in range(decimal_places):
        quantize_spec_list.append("0")
    quantize_spec_string = "".join(quantize_spec_list)
    quantized_value = value.quantize(Decimal(quantize_spec_string))
    return int(quantized_value * Decimal(factor))

def monetary_float_to_int(value, app_config):
    '''Convert a float representation of a monetary quantity, e.g., a price 
    to an integer.
    
    Monetary quantities are returned as floats from widgets like line edits, 
    and are converted using this function into integers for storage in the 
    database. 
    
    The number of decimal places used by the currency is configurable. This 
    function multiplies the supplied float by a factor corresponding to the 
    required number of decimal places, and converts the result to integer.
    
    Args:
    :param value: The monetary value to convert to integer.
    :type value: Float
    :param app_config: The application configuration in use.
    :type app_confg: appconfig.ConfigFile
    
    Returns:
    :return: The monetary value as an integer.
    :rtype: Integer
    
    Raises:
    :raises: AssertionError if value is not a Decimal.
    '''
    assert type(value) == float
    # Calculate the factor from the configured decimal places.
    decimal_places = int(app_config.locale.currency_decimal_places)
    factor = 10 ** decimal_places
    # Round the value the correct number of decimal places before converting to 
    # integer.
    quantize_spec_list = ["1."]
    for d in range(decimal_places):
        quantize_spec_list.append("0")
    quantize_spec_string = "".join(quantize_spec_list)
    quantized_value = Decimal(value).quantize(Decimal(quantize_spec_string))
    return int(quantized_value * Decimal(factor))

if __name__ == '__main__':
    # Test percentage_int_to_decimal
    print("Testing that percentage_int_to_decimal converts 14 to 0.14...")
    assert percentage_int_to_decimal(14) == Decimal("0.14")
    print("Pass")
    
    # Test percentage_decimal_to_int
    print("Testing that percentage_decimal_to_int converts 0.14 to 14...")
    assert percentage_decimal_to_int(Decimal("0.14")) == 14
    print("Pass")
    
    # Test monetary_int_to_decimal
    from appconfig import ConfigFile
    test_app_config = ConfigFile()
    test_app_config.load()
    test_app_config.locale.currency_decimal_places = 0
    print("Testing that monetary_int_to_decimal converts 12345 to 12345 when "
          "currency decimal places is 0...")
    assert monetary_int_to_decimal(12345, test_app_config) == Decimal("12345")
    print("Pass")
    test_app_config.locale.currency_decimal_places = 1
    print("Testing that monetary_int_to_decimal converts 12345 to 1234.5 when "
          "currency decimal places is 1...")
    assert monetary_int_to_decimal(12345, test_app_config) == Decimal("1234.5")
    print("Pass")
    test_app_config.locale.currency_decimal_places = 2
    print("Testing that monetary_int_to_decimal converts 12345 to 123.45 when "
          "currency decimal places is 2...")
    assert monetary_int_to_decimal(12345, test_app_config) == Decimal("123.45")
    print("Pass")
    test_app_config.locale.currency_decimal_places = 3
    print("Testing that monetary_int_to_decimal converts 12345 to 12.345 when "
          "currency decimal places is 3...")
    assert monetary_int_to_decimal(12345, test_app_config) == Decimal("12.345")
    print("Pass")
    test_app_config.locale.currency_decimal_places = 4
    print("Testing that monetary_int_to_decimal converts 12345 to 1.2345 when "
          "currency decimal places is 4...")
    assert monetary_int_to_decimal(12345, test_app_config) == Decimal("1.2345")
    print("Pass")
    
    # Test monetary_decimal_to_int
    test_app_config.locale.currency_decimal_places = 0
    print("Testing that monetary_decimal_to_int converts 12345 to 12345 when "
          "currency decimal places is 0...")
    assert monetary_decimal_to_int(Decimal("12345"), test_app_config) == 12345
    print("Pass")
    test_app_config.locale.currency_decimal_places = 1
    print("Testing that monetary_decimal_to_int converts 1234.5 to 12345 when "
          "currency decimal places is 1...")
    assert monetary_decimal_to_int(Decimal("1234.5"), test_app_config) == 12345
    print("Pass")
    test_app_config.locale.currency_decimal_places = 2
    print("Testing that monetary_decimal_to_int converts 123.45 to 12345 when "
          "currency decimal places is 2...")
    assert monetary_decimal_to_int(Decimal("123.45"), test_app_config) == 12345 
    print("Pass")
    test_app_config.locale.currency_decimal_places = 3
    print("Testing that monetary_decimal_to_int converts 12.345 to 12345 when "
          "currency decimal places is 3...")
    assert monetary_decimal_to_int(Decimal("12.345"), test_app_config) == 12345 
    print("Pass")
    test_app_config.locale.currency_decimal_places = 4
    print("Testing that monetary_decimal_to_int converts 1.2345 to 12345 when "
          "currency decimal places is 4...")
    assert monetary_decimal_to_int(Decimal("1.2345"), test_app_config) == 12345 
    print("Pass")