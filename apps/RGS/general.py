class getModel():
    # Variables
    model = None  # Chosen model
    all_models = {}  # Dictionary with all the models
    verbose_models_names = []  # A list with the verbose names of the models
    foreign_keys = []  # List of all the foreign keys of the model

    # Constructor
    def __init__(self, model_name: str, dict_models, verbose_models_names):
        # Initialize variables
        self.all_models = dict_models
        self.verbose_models_names = verbose_models_names

        # Get the model
        self.get_model(model_name)

        # Get all the foreign keys of the model
        self.get_fks()

    # Get the model
    def get_model(self, model_name: str):
        if model_name in self.verbose_models_names:
            # Position in list
            pos = self.verbose_models_names.index(model_name)
            # Find the model
            index = 0
            found = False
            for item in self.all_models:  # This way only possible since it is an ordered dictionary
                if index == pos:
                    self.model = self.all_models[item]
                    found = True
                    break
                else:
                    index = index + 1
            if not found:
                raise ValueError("Selected model not found!")
        else:
            raise ValueError("No selected model!")

    # Get all foreign keys of the model
    def get_fks(self):
        for field in self.model._meta.fields:
            if field.get_internal_type() == 'ForeignKey':
                self.foreign_keys.append(field)
