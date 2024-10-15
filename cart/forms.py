from django import forms



PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]

PERSON_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 5)]

class CartAddProductForm(forms.Form):

    
    product_desc = forms.CharField(
    required=False,
    label="",  # Set the label
    widget=forms.Textarea(attrs={
        'readonly': 'readonly',
        'style': 'border: none; background: none; width: 100%; height: auto; max-height: 200px; overflow-y: auto;resize: none;',  # Adjust for more rows
        'rows': '9',  # Set the number of visible rows
        'wrap': 'soft'
    })
    )


    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int)
    

    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)
    
    #  For shop 1

    revised_price = forms.DecimalField(
        required=False,
        label="",  # Set the label
        widget=forms.NumberInput(attrs={
        'readonly': 'readonly',
        'style': 'border: none; background: none; width: 100%;',  # Adjust as needed
        'step': '0.01',  # Allows for decimal input
        'value': '0.00'  # You can set a default value here if needed
        })
        )
    
    
    

