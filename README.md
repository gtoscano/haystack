#  Haystack module

This module is a small modification to  [José de Soto's web2py-haystack-module](https://github.com/josedesoto/web2py-haystack-module), which in turn, was based on [Massimo Di Pierro's plugin](https://github.com/mdipierro/web2py-haystack).

This modification updates de Soto's module to work with Python3 and includes a reindex method, which can be of value when you want to index previously stored data.

Usage:
```
# model
db = DAL()
db.define_table('thing',Field('name'),Field('description'))

# call the module
index = Haystack(db.thing, core="things")         # table to be indexed
index.indexes('name','description')               # fields to be indexed
db.thing.insert(name='Char',description='A char') # automatically indexed
db(db.thing.id).update(description='The chair')   # automatically re-indexed
db(db.thing).delete()                             # automatically re-indexed
query = index.search(name='chair',description='the')
print db(query).select()
```

In addition, the new module can index previously stored entries. The following example will index all data in table thing.

```
index.index_table((db.thing.id > 0) , db)

```

For more info about options refer to [José de Soto's web2py-haystack-module](https://github.com/josedesoto/web2py-haystack-module)



# Changes
## layout.html
```
	<form class="form-inline my-2 my-lg-0">
             <input class="form-control mr-sm-2" type="text"  id="inputsearchform" placeholder="Search" >
	</form>
```

at the end of layout.html
```
	<script>
	function search(my_input){
        var dest = "{{=URL('default', 'my_search')}}";
        location.href = dest+"/"+my_input;
      }
      
      var myinput = document.getElementById("inputsearchform");
      myinput.addEventListener('keypress', function(ev){

        if(ev.keyCode === 13 || ev.which === 13){
          ev.preventDefault(); 
          search(myinput.value);
          return false;
        }
        return true;
      });
    </script>
```