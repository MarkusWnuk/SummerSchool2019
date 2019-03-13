from threading import Lock

class One_Dim_Value:
    """ Defines a lockable one dimensional Variable

    Attributes:
        value (float): Human readable string describing the exception.
        name (str): Human readable string naming the class.

    """

    def __init__(self, name):
        """
        Initializes the variable with the value of 0.0
        Args:
            name (str): Human readable string naming the class.
        """
        self.name = name
        self.value = 0.0
        self.lock = Lock()

    def read_value(self):
        """To read the value of the object. Value is locked during the readout
            Raises:
                TODO: Error handling
            Returns:
              value of the object.
            """
        self.lock.acquire()
        output = self.value
        self.lock.release()
        return output

    def write_value(self, inputvalue):
        """To write the value of the object. Value is locked during the writing process
            Args:
                inputvalue: that is written into self.value
            Raises:
                TODO: Error handling
            Returns:
              value of the object.
            """
        self.lock.acquire()
        self.value = inputvalue
        self.lock.release()


class Locked_Values:
    """ Defines a lockable more dimensional Variable

    Attributes:
        value (float): Human readable string describing the exception.
        name (str): Human readable string naming the class.
        dimensions(int): Number of dimensions

    """

    def __init__(self, name, dimensions):
        """
        Initializes the variable with the value of 0.0
        Args:
            name (str): Human readable string naming the class.
            dimensions(int): Number of dimensions
        """
        self.name = name
        self.dimensions = dimensions
        self.values = [0.0]*dimensions
        self.lock = Lock()

    def read_value(self):
        """To read the value of the object. Value is locked during the readout
            Raises:
                TODO: Error handling
            Returns:
              value of the object.
            """
        self.lock.acquire()
        output = self.values
        self.lock.release()
        return output

    def write_value(self, inputvalues):
        """To write the value of the object. Value is locked during the writing process
            Args:
                inputvalue: that is written into self.value
            Raises:
                TODO: Error handling
            Returns:
              value of the object.
            """

        if len(inputvalues) == self.dimensions:
            self.lock.acquire()
            self.values = inputvalues
            self.lock.release()
        else:
            raise Exception('Error: Dimensions of write value should be: ' + str(self.dimensions))