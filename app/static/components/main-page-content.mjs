import {Component, html, createRef} from "../preact.mjs";
import {CheckingSettings} from "./checking-settings.mjs";
import {ReportsList} from "./reports-list.mjs";
import {PresentationUploadingArea} from "./presentation-uploading-area.mjs";
import {stateSaving, createStateSaver} from "../state-saving.mjs";

export class MainPageContent extends stateSaving(Component) {
    constructor(props) {
        super(props);

        this.state = {};

        if (!this.restoreState())
            this.state._checkingSettingsStateSaver = createStateSaver();

        this._mainPageContentRootRef = createRef();
    }

    componentDidMount() {
        if (this.state.scrollTop) {
            this._mainPageContentRootRef.current.parentElement.scrollTop = this.state.scrollTop;
            delete this.state.scrollTop;
        }
    }
    componentWillUnmount() {
        this.state.scrollTop = this._mainPageContentRootRef.current.parentElement.scrollTop;
        super.componentWillUnmount();
    }

    render() {
        return html`
            <div ref=${this._mainPageContentRootRef} class="main-block">
                <${PresentationUploadingArea} getSettings=${() => this._getSettings()}/>
                <${CheckingSettings} getSettingsCallback=${getSettings => this._getSettings = getSettings}
                    stateSaver=${this.state._checkingSettingsStateSaver}/>
                <${ReportsList} />
            </div>
        `;
    }
}