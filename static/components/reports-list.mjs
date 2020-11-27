import {html, useContext} from "../preact.mjs";
import {Link} from "./link.mjs";
import {AppContext} from "./app.mjs";

export function ReportsList(props) {
    const app = useContext(AppContext);

    if (!app.isLoggedIn())
        return html``;

    let reportsElements;

    if (app.state.reports === undefined) {
        app.fetchReports();
        reportsElements = html`<div class="loading"></div>`;
    }
    else if (app.state.reports.length === 0) {
        reportsElements = html`<div class="subtle-text">Пока пусто</div>`;
    }
    else {
        reportsElements = app.state.reports.map(report => html`
            <${Link} class="report-link" href=${"/report/" + report.id}>
                <div>${report.fileName}</div>
                <div>${new Date(report.datetime).toLocaleString()}</div>
            <//>
        `);
    }

    return html`
        <h2>Прошлые проверки</h2>
        ${reportsElements}
    `;
}