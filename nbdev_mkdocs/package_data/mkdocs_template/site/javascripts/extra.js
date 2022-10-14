document.addEventListener("DOMContentLoaded", function(event) { 
    
    const MODULE_NAME = "airt.client"
    
    var _toc_nav_items = document.querySelectorAll(".md-sidebar--secondary .md-nav > .md-nav__list > .md-nav__item > a")
    
    var page_identifier = document.querySelectorAll('.md-tabs ul > li > a.md-tabs__link--active')[0].innerText

    var _base_path = (page_identifier == 'Home') ? "./API/client/" : ((page_identifier == 'Tutorial') ? "../API/client/" : "../" )

    var current_class_methods = []
    
    _toc_nav_items.forEach((item) => current_class_methods.push( {"name": item.innerHTML.trim(),"href" : item.href.split("/").at(-1)} ));
    
    function generate_anchor_tag(obj) {
        label = obj.innerHTML
        current_class_object = current_class_methods.find(item => item.name.split("()")[0] == label)
        
        if (current_class_object) {
           _new_tag = "<a href='"+current_class_object.href+"'>" + label + "</a>";
        }
        else {
            if (label.split(".").length == 1)  { 
                _temp_url = _base_path+label+"/"
                _new_tag = '<a href='+_temp_url+' />'+label+'</a>'
            } 
            else if (label.split(".").length > 1) {
              _temp_url = _base_path+label.split(".")[0]+"#"+MODULE_NAME+"."+label
              _new_tag = '<a href='+_temp_url+' />'+label.split(".")[1]+'</a>'
            }
        }   
        
        obj.innerHTML = _new_tag
    }
       
    // Add hyperlinks across the site
    var _objects = document.querySelectorAll(".md-content > article p > code")
    _objects.forEach(generate_anchor_tag)
});