import {html, useContext} from "../preact.mjs";
import {Link} from "./link.mjs";
import {AppContext} from "./app.mjs";

export function ReportsList(props) {
    const app = useContext(AppContext).app;

    if (!app.isLoggedIn())
        return html``;

    if (!app.state.reports || !app.state.reports.length) {
        app.fetchReports();
        return html``;
    }

    return html`
        <h2>Прошлые проверки</h2>
        ${
            app.state.reports.map(report => html`
                <${Link} class="report-link" href=${"/report/" + report.id}>
                    <div>${report.fileName}</div>
                    <div>${new Date(report.datetime).toLocaleString()}</div>
                <//>
            `)
        }
    `;
}