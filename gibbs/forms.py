from django import forms
from gibbs import constants

class ListFormField(forms.MultipleChoiceField):
    """
        A form field for a list of values that are unchecked.
        
        The Django MultipleChoiceField does *almost* what we want, except
        it validates that each choice is in a supplied list of choices, 
        even when that list is empty. We simply override the validation.
    """
    
    def valid_value(self, value):
        return True
 
class EnzymeForm(forms.Form):
    ec = forms.CharField(max_length=50)
    
    # Convenience accessors for clean data with defaults.
    cleaned_ec = property(lambda self: self.cleaned_data['ec'])
       
class SearchForm(forms.Form):
    def _GetWithDefault(self, key, default):
        if (key not in self.cleaned_data or
            self.cleaned_data[key] == None):
            return default
        return self.cleaned_data[key]
    
    query = forms.CharField(max_length=2048, required=False)
    ph = forms.FloatField(required=False)
    pmg = forms.FloatField(required=False)
    ionic_strength = forms.FloatField(required=False)
    electronReductionPotential = forms.FloatField(required=False)
    
    # Convenience accessors for clean data with defaults.
    cleaned_query = property(lambda self: self._GetWithDefault('query', ''))
    cleaned_ph = property(lambda self: self._GetWithDefault('ph', None))
    cleaned_pmg = property(lambda self: self._GetWithDefault('pmg', None))
    cleaned_ionic_strength = property(lambda self: self._GetWithDefault('ionic_strength', None))
    cleaned_e_reduction_potential = property(lambda self: self._GetWithDefault('electronReductionPotential', None))

class ReactionForm(SearchForm):
    
    def GetReactantConcentrations(self):
        prefactors = map(float, self.cleaned_data['reactantsConcentrationPrefactor'])

        for f, c in zip(prefactors, self.cleaned_data['reactantsConcentration']):
            try:
                conc = f * float(c)
                if conc <= 0:
                    yield 1e-9
                else:
                    yield conc
            except ValueError:
                yield 1e-9
                
    reactionId = forms.CharField(required=False)
    reactantsId = ListFormField(required=False)
    reactantsCoeff = ListFormField(required=False)
    reactantsName = ListFormField(required=False)
    reactantsPhase = forms.MultipleChoiceField(required=False,
                                               choices=constants.PHASE_CHOICES)
    reactantsConcentration = ListFormField(required=False)
    reactantsConcentrationPrefactor = ListFormField(required=False)
    conditions = forms.ChoiceField(required=False,
                                   choices=constants.CONDITION_CHOICES)
    
    submit = forms.ChoiceField(required=False,
                               choices=[('Update', 'update'),
                                        ('Save', 'save'),
                                        ('Reverse', 'reverse')])
    
    # Convenience accessors for clean data with defaults.
    cleaned_reactionId = property(lambda self: self.cleaned_data['reactionId'])
    cleaned_reactantsId = property(lambda self: self.cleaned_data['reactantsId'])
    cleaned_reactantsCoeff = property(lambda self: [float(c) for c in self.cleaned_data['reactantsCoeff']])
    cleaned_reactantsName = property(lambda self: self.cleaned_data['reactantsName'])
    cleaned_reactantsPhase = property(lambda self: self.cleaned_data['reactantsPhase'])
    cleaned_reactantsConcentration = property(GetReactantConcentrations)
    cleaned_conditions = property(lambda self: self.cleaned_data['conditions'])
    cleaned_submit = property(lambda self: self._GetWithDefault('submit', 'Update'))

class ReactionGraphForm(ReactionForm):
    vary_ph = forms.BooleanField(required=False)
    vary_is = forms.BooleanField(required=False)
    vary_pmg = forms.BooleanField(required=False)
    
    # Convenience accessors for clean data with defaults.
    cleaned_vary_ph  = property(lambda self: self._GetWithDefault('vary_ph', False))
    cleaned_vary_pmg = property(lambda self: self._GetWithDefault('vary_pmg', False))
    cleaned_vary_is  = property(lambda self: self._GetWithDefault('vary_is', False)) 
    
class CompoundForm(SearchForm):
   
    def GetReactantConcentrations(self):
        for c in self.cleaned_data['reactantsConcentration']:
            try:
                conc = float(c)
                if conc <= 0:
                    yield 1e-9
                else:
                    yield conc
            except ValueError:
                yield 1e-9

    def GetReactantPhases(self):
        for p in self.cleaned_data['reactantsPhase']:
            if p == '':
                yield None
            else:
                yield p

    compoundId = forms.CharField(max_length=50)
    reactantsPhase = forms.MultipleChoiceField(required=False,
                                               choices=constants.PHASE_CHOICES)
    reactantsConcentration = ListFormField(required=False)
    conditions = forms.ChoiceField(required=False,
                                   choices=constants.CONDITION_CHOICES)

    # Convenience accessors for clean data with defaults.
    cleaned_compoundId = property(lambda self: self.cleaned_data['compoundId'])

    # we need to create the following properties in order for this form
    # to impersonate a reaction_form (something we need to do for creating
    # a Reaction object using .FromForm(form))
    cleaned_reactionId = property(lambda self: None)
    cleaned_reactantsId = property(lambda self: [self.cleaned_compoundId])
    cleaned_reactantsCoeff = property(lambda self: [1])
    cleaned_reactantsName = property(lambda self: [None])
    cleaned_reactantsPhase = property(GetReactantPhases)
    cleaned_reactantsConcentration = property(GetReactantConcentrations)
    cleaned_conditions = property(lambda self: self.cleaned_data['conditions'])