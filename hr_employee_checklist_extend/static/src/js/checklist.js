 openerp.hr_employee_checklist_extend = function (instance) {
 	var QWeb = instance.web.qweb,
    _t = instance.web._t;

    //console.log('2222');
    
    instance.web.FormView.include({
    	load_form: function(data) {
    		self = this;
    		this._super(data);
    		var AutoclickEdit;
    		clearTimeout(AutoclickEdit);

			AutoclickEdit = setTimeout(function(){
	    		//console.log(this);
	    		if(self.fields_view.arch.tag == "form"){
	    			//console.log($("div.oe_list.oe_view.oe_cannot_create.oe_cannot_delete.oe_list_editable >table.oe_list_content > thead >tr.oe_list_header_columns >th.oe_list_header_many2one.oe_sortable"));
	    			//console.log($("th[data-id='param_name_1_related']"));

	    			//console.log($("td[data-field='param_name_1_related']"));
		    		$("th[data-id='param_name_1_related']").attr('colspan', '9');
		    		$("th[data-id='param_name_1_related']").css('text-align', 'center');
					$("th[data-id='param_name_2_related']").remove();
					$("th[data-id='param_name_3_related']").remove();    		    			
					$("td[data-field='param_name_1_related']").each(function( index ) {
						$(this).css('width','20%');
					});
					$("td[data-field='param_name_1_value']").each(function( index ) {
						$(this).css('width','8%');
					});	
					$("td[data-field='param_name_3_value']").each(function( index ) {
						$(this).css('width','8%');
					});					


	    			//$("td[data-field='param_name_1_related']").css('width','20%');	

	    		}
			}, 500);
    	}
    });
    /*
    instance.web.form.FieldOne2Many.include({
	    init: function(field_manager, node) {
	        this._super(field_manager, node);
	        this._Remove_column_headers();
	    },    	
	    _Remove_column_headers: function(){
	        $('th[data-id="param_name_1_value"]').remove();
	        $('th[data-id="param_name_1_check"]').remove();
	        $('th[data-id="param_name_2"]').remove();
	        $('th[data-id="param_name_2_value"]').remove();
	        $('th[data-id="param_name_2_check"]').remove();
	        $('th[data-id="param_name_3"]').remove();
	        $('th[data-id="param_name_3_value"]').remove();
	        $('th[data-id="param_name_3_check"]').remove();
	        $('th[data-id="param_name_1"]').attr("colspan", "9"); 
	        $('th[data-id="param_name_1"] > div').attr("align", "center");
	        $('table[class="oe_list_content"]>tfoot>tr').remove()
	        //throw x;
	        //return true;

    		$("th[data-id='param_name_1_related']").attr('colspan', '9');
    		$("th[data-id='param_name_1_related']").css('text-align', 'center');
			$("th[data-id='param_name_2_related']").remove();
			$("th[data-id='param_name_3_related']").remove();    		    			
			$("td[data-field='param_name_1_related']").each(function( index ) {
				$(this).css('width','20%');
			});
			$("td[data-field='param_name_1_value']").each(function( index ) {
				$(this).css('width','8%');
			});	
			$("td[data-field='param_name_3_value']").each(function( index ) {
				$(this).css('width','8%');
			});			        
	     },
	    
	    reload_current_view: function() {
	        var self = this;
	        this._super();
	        self._Remove_column_headers();
	        //return this._super();
	    },	
	    set_value: function(value_) {
	        value_ = value_ || [];
	        var self = this;
	        this._super(value_);
	        if (this.is_started && !this.no_rerender) {
	            return self.reload_current_view();
	        } else {
	            self._Remove_column_headers();
	            return $.when();
	        }
	    },	      
    });*/

 }