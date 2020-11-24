import {Component, html} from '../preact.mjs';
import {studentDegreesWithPrintable, studentDegreesWithPrintableArray} from "./app.mjs";
import {Switch} from "./switch.mjs";

export class CheckingSettings extends Component {
    get settings() {
        return {
            studentDegree: this.state.studentDegree,
        };
    }

    render() {
        return html`
            <div class=${"toggle " + (this.state.open ? "open" : "")}>
                <div class="toggle-header" onclick=${() => this.setState({open: !this.state.open})}>
                    <div class="toggle-indicator">▼</div>
                    <div>Настройки проверки</div>
                    <div class="toggle-short-content">${studentDegreesWithPrintable[this.state.studentDegree]}</div>
                </div>
                <div class="toggle-content">
                    <${Switch} valuesWithPrintable=${studentDegreesWithPrintableArray()}
                        onSwitch=${studentDegree => this.setState({studentDegree})} />
                </div>
            </div>
        `;
    }
}