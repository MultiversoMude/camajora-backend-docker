odoo.define('rental.CalendarView', function (require) {
"use strict";


    var CalendarView = require('web.CalendarView');
    CalendarView.include({
         _getFullCalendarOptions: function () {
            var res = this._super.apply(this, arguments);
            return _.extend(res, {
                minTime: '08:00:00',
                maxTime: '22:00:00',
                slotDuration: '00:10:00',
            });
        },
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