from django.forms import ModelForm, TextInput, CharField, PasswordInput, NumberInput



from . import models

class CreateRegisterForm(ModelForm):
    # add password confirmation field 
    password_confirmation = CharField(     
    widget=PasswordInput(attrs={'placeholder': 'Confirm Password', 'autocomplete':'off'}),
    required=True,
    )

    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'tip', 'email', 'password']        
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': TextInput(attrs={'placeholder': 'Last Name'}),
            'tip': NumberInput(attrs={'placeholder': 'Default Tip %'} ),
            'email': TextInput(attrs={'placeholder': 'Email Address'}),
            'password': PasswordInput(attrs={'placeholder': 'Password','autocomplete':'off'} ), 
        }
             

    def __init__(self, *args, **kwargs): 
        edit = kwargs.pop('edit', False) 
        update_password  = kwargs.pop('update_password', False)     
        super().__init__(*args, **kwargs)   
        if edit:          
            del self.fields['email']
            del self.fields['password']
            del self.fields['password_confirmation']
        if update_password:
            del self.fields['first_name']
            del self.fields['last_name']
            del self.fields['tip']
            del self.fields['email']
            self.fields['password'].widget.attrs.update({'placeholder': 'New Password'})

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class BillForm(ModelForm):    
    class Meta:
        model = models.Bill_Header
        fields = ['title','tip','tax','discount']
        widgets = {
            'title': TextInput(attrs={'placeholder': 'Title'}),
            # 'total': NumberInput(attrs={'placeholder': 'Bill Total'}),
            'tip': NumberInput(attrs={'placeholder': 'Tip %'}),
            'tax': NumberInput(attrs={'placeholder': 'Tax %'}),
            'discount': NumberInput(attrs={'placeholder': 'Discount %'}),               
             
        } 
        labels = {
            # 'split': "Split bill evenly",
            'tip': "Tip%",
            'tax': "Tax%",
            'discount': "Disc%",
        }      

    def __init__(self, *args, **kwargs):
        edit = kwargs.pop('edit', False) 
        kwargs["label_suffix"] = ""         
        super().__init__(*args, **kwargs)       
                
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        # self.fields['split'].widget.attrs.update({'class': 'form-check-input'})


class BillDetailForm(ModelForm):
    class Meta:
        model = models.Bill_Lines
        fields = ['item','quantity','total','discount']
        widgets = {
                'item': TextInput(attrs={'placeholder': 'Item'}),
                'quantity': NumberInput(attrs={'placeholder': 'Qauntity'}),
                'total': NumberInput(attrs={'placeholder': 'Total'}), 
                'discount': NumberInput(attrs={'placeholder': 'Discount %'}),                    
            } 
         

    def __init__(self, *args, **kwargs):               
            super().__init__(*args, **kwargs)  
            for field in self.fields:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })


class BillUserForm(ModelForm):
    class Meta:
        model = models.Bill_User
        fields = ['name','tip', 'id']
        widgets = {
                'name': TextInput(attrs={'placeholder': 'Name'}),
                'tip': NumberInput(attrs={'placeholder': 'User Tip %'}),
                'id': NumberInput()
            }            

    def __init__(self, *args, **kwargs):               
            super().__init__(*args, **kwargs)  
            for field in self.fields:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })                

class ImageForm(ModelForm):
    class Meta:
        model = models.Bill_Header
        fields = ['image']

