odoo.define('rental.CalendarView', function (require) {
"use strict";


    var CalendarView = require('web.CalendarView');
    CalendarView.include({
        init: function (viewInfo, params) {
            this._super.apply(this, arguments);
            if (this.controllerParams.modelName == 'rental.booking.slot') {
                this.loadParams.editable = false;
                this.loadParams.creatable = false;
            }
        },
    });

    return CalendarView;
});