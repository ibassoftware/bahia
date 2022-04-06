
 openerp.bahia_personnel_management = function (instance) {
    instance.web.form.custom_widgets.add('one2many_remove_spec_columns','instance.bahia_personnel_management.one2many_remove_spec_columns');
    //instance.web.list.columns.add('field.one2many_remove_spec_columns', 'instance.bahia_personnel_management.one2many_remove_spec_columns');
    instance.bahia_personnel_management.one2many_remove_spec_columns = instance.web.form.FieldOne2Many.extend({
        _start: function() {
            this._super.apply(this, arguments);
            //var amount = parseFloat(res);
            //return "<font color='#0000CD'>"+amount.toFixed(2)+"</font>";
            //return "<font color='#8B0000'>"+amount.toFixed(2)+"</font>";
            //return amount.toFixed(2);
	    throw "YAHOO";
	    //$('p[data-id="stand-out"]').remove();
	    //document.getElementById("myTable").remove();

        }
    });

    instance.web.list.columns.add('field.on2manyrem', 'instance.bahia_personnel_management.on2manyrem');
    instance.bahia_personnel_management.on2manyrem = instance.web.list.Column.extend({
        _format: function (row_data, options) {
            //res = this._super.apply(this, arguments);
            //var amount = parseFloat(res);
            //return "<font color='#0000CD'>"+amount.toFixed(2)+"</font>";
            //return "<font color='#8B0000'>"+amount.toFixed(2)+"</font>";
	    console.log('on2manyrem');
	    throw "YAHOO";
            //return amount.toFixed(2);
        }
     )};

};

