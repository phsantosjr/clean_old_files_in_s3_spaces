class PrefixNameFolderNotFoundException(Exception):
    def __str__(self):
        return "Folder/Prefix name was not found ! We need it to process !"


class MonthInformedIsNotIntException(Exception):
    def __str__(self):
        return "Please put a positive integer number !"
