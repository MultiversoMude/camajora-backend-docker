odoo.define('rental.web_widget_seconds_to_hours', function (require) {
"use strict";

    var AbstractField = require('web.AbstractField');
    var field_registry = require('web.field_registry');

    var HourField  = AbstractField.extend({
        supportedFieldTypes: ['integer'],
        init: function () {
            this._super.apply(this, arguments);

        },
        _transformSecondsToHours(value){
            var seconds = parseInt(value, 10);
            var hrs   = Math.floor(seconds / 3600);
            seconds  -= hrs*3600;
            var mnts = Math.floor(seconds / 60);
            return hrs+':'+mnts;
        },
        _renderReadonly: function () {
            this.$el.empty().text(this._transformSecondsToHours(this.value));
        }
    });
     field_registry.add('hourseconds', HourField);
      return {
        HourField: HourField,
    };
});