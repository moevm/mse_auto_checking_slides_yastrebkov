import {Component, html, useContext} from "../preact.mjs";
import {AppContext, App, studentDegreesWithPrintable} from "./app.mjs";
import {get} from "../ajax.mjs";

export class ReportView extends Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    _fetchReport() {
        if (this._app.state.reports) {
            let report = this._app.state.reports.find(report => report.id === this.props.reportId);
            if (report) {
                this.setState({responseWithReport: {success: true, report}});
                return;
            }
        }

        get("/api/report/" + this.props.reportId)
        .then(responseWithReport => {
            if (!responseWithReport)
                return;
            this.setState({responseWithReport});
        });
    }

    render() {
        this._app = useContext(AppContext);

        if (!this.state.responseWithReport) {
            this._fetchReport();
            return html`<div class="loading report" ></div>`;
        }

        if (!this.state.responseWithReport.success)
            return html`<div class="banner">Такая проверка не найдена :(</div>`;

        let report = this.state.responseWithReport.report;

        let studentDegree = null;
        if ('studentDegree' in report)
            studentDegree = html`<div>${studentDegreesWithPrintable[report.studentDegree]}</div>`;

        const checkToElement = check => {
            let checkName = html([check.name.replace(/"(.*)"/g, '<span class=fragment>$1</span>')]);
            return html`
                <div class="check">
                    <div class=${check.success ? "success-sign" : "fail-sign"} />
                    <div>${checkName}</div>
                </div>
            `;
        };

        return html`
            <div class="report">
                <div>${new Date(report.datetime).toLocaleString()}</div>
                <samp>${report.fileName}</samp>
                ${studentDegree}
                <div class="checks">${report.checks.map(checkToElement)}</div>
            </div>
        `;
    }
}