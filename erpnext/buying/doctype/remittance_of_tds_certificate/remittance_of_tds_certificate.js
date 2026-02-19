// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Remittance of TDS certificate', {
    refresh: function(frm) {
        frm.get_field("import_log_preview").$wrapper.html("")
        if(frm.doc.workflow_state==='Pending'){
            $('.actions-btn-group').prop('hidden', true);
        }
        if (!frm.is_dirty()) {
            
            frm.add_custom_button(__('Send Email'), function() {
                // console.log("clicked")
                frm.call('unpack')
                .then(r => {
                    if (r.message === 1) {
                        console.log("worked")
                        frm.save('Submit');
                       //do something
                    }
                });
            }).addClass("btn-warning").css({'background-color':'red','font-weight': 'bold'});
        }
        if(frm.doc.docstatus === 1){
        frm.remove_custom_button('Send Email')
        frm.trigger("import_log_preview")}
    },

    import_log_preview: function(frm) {
            let logs = frm.doc.error_logs;
            let html = "";
            if(frm.doc.error_logs){
                if (logs.length === 0) return;
                let rows = logs.map(log => {
                    html = "";
                    if (log.status) {
                        let messages = log.reason;
                        let id = frappe.dom.get_unique_id();
                        html = `${messages}
                        <br>
                <button class="btn btn-default btn-xs" type="button" data-toggle="collapse" data-target="#${id}" aria-controls="${id}" 
                style="margin-top: 15px;">
                ${__("Show Traceback")}
                </button>
                <div class="collapse" id="${id}" style="margin-top: 15px;">
                <div class="well">
                <pre>${log.reason}</pre>
                </div>
                </div>`;
            }
            
            let indicator_color = log.status !== "Failure" ? "green" : "red";
            let title = log.status !== "Failure" ? __("Success") : __("Failure");
            let message_log = log.status !== "Failure" ? __("Email Sent Successfully") : __("Email Not Sent to Supplier");
            
            return `<tr>
            <td>${log.name}</td>
            <td>
            <div class="indicator ${indicator_color}">${title}</div>
            </td>
            <td>
            ${html}
            </td>
            <td>${message_log}</td>
            </tr>`;
        }).join("");
        
        if (!rows) {
            rows = `<tr><td class="text-center text-muted" colspan="3">
            ${__("No failed logs")}
            </td></tr>`;
        }
        
        frm.get_field("import_log_preview").$wrapper.html(`
        <table class="table table-bordered">
        <tr class="text-muted">
        <th width="10%">${__("ID")}</th>
        <th width="10%">${__("Status")}</th>
        <th width="50%">${__("Message")}</th>
        <th width="30%">${__("Response")}</th>
        </tr>
        ${rows}
        </table>
        `);
    }
}
});