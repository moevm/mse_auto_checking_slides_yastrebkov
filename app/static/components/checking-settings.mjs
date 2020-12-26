import {Component, html} from '../preact.mjs';
import {studentDegreesWithPrintable, studentDegreesWithPrintableArray} from "./app.mjs";
import {Switch} from "./switch.mjs";
import {createStateSaver, stateSaving} from "../state-saving.mjs";

export class CheckingSettings extends stateSaving(Component) {
    constructor(props) {
        super(props);

        this.state = {studentDegree: 'bachelor'};

        if (!this.restoreState())
            this.state._studentDegreeSwitchStateSaver = createStateSaver();

        this.props.getSettingsCallback(this.getSettings.bind(this));
    }

    getSettings() {
        return {
            studentDegree: this.state.studentDegree
        }
    }

    render() {
        return html`
            <div class=${"toggle " + (this.state.open ? "open" : "")}>
                <div class="toggle-header" onclick=${() => this.setState({open: !this.state.open})}>
                    <div class="toggle-indicator">▼</div>
                    <div>Настройки проверки</div>
                    <div class="toggle-short-content">
                        ${studentDegreesWithPrintable[this.state.studentDegree]}
                    </div>
                </div>
                <div class="toggle-content">
                    <${Switch} value=${this.state.studentDegree}
                        valuesWithPrintable=${studentDegreesWithPrintableArray()}
                        onSwitch=${studentDegree => this.setState({studentDegree})} />
                </div>
            </div>
        `;
    }
}