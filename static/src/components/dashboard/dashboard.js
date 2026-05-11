/** @odoo-module */

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class NurseryDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            stats: {
                company_name: '',
                total_students: 0,
                total_present: 0,
                average_mood: 'N/A',
                has_fee_access: false,
                fee_received: 0.0,
                upcoming_events: []
            }
        });

        onWillStart(async () => {
            await this.loadStats();
        });
    }

    async loadStats() {
        const result = await this.orm.call("nursery.dashboard", "get_dashboard_stats", []);
        this.state.stats = result;
    }

    openStudents() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Students",
            res_model: "nursery.student",
            views: [[false, "list"], [false, "form"]],
        });
    }

    openFees() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Fees",
            res_model: "nursery.fee",
            domain: [['state', '=', 'posted']],
            views: [[false, "list"], [false, "form"]],
        });
    }

    openCheckin() { this.action.doAction("nursery_management.action_nursery_checkin"); }
    openAttendanceReport() { this.action.doAction("nursery_management.action_nursery_attendance_report_wizard"); }
    openEvents() { this.action.doAction("nursery_management.action_nursery_event"); }
    openNotices() { this.action.doAction("nursery_management.action_nursery_notice"); }
    openSuggestions() { this.action.doAction("nursery_management.action_nursery_suggestion"); }
}

NurseryDashboard.template = "nursery_management.Dashboard";

registry.category("actions").add("nursery.dashboard", NurseryDashboard);
