import {Component, html, useContext, createRef} from "../preact.mjs";
import {post} from "../ajax.mjs";
import {CheckingSettings} from "./checking-settings.mjs";
import {ReportsList} from "./reports-list.mjs";
import {AppContext} from "./app.mjs";

function toBase64(file){
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
            let result = reader.result;
            resolve(result.substring(result.indexOf(",") + 1));
        }
        reader.onerror = error => reject(error);
    });
}

export class MainPageContent extends Component {
    constructor(props) {
        super(props);

        this._checkingSettingsRef = createRef();
    }

    _uploadPresentationForChecking(file) {
        if (!file)
            return;

        toBase64(file).then(presentation => {
            post("/api/check-presentation", {
                presentation,
                fileName: file.name,
                ...this._checkingSettingsRef.current.settings
            })
            .then(response => {
                if (!response || !response.success)
                    return;
                this._app.relocate('/report/' + response.reportId);
                this._app.fetchReports(); // TODO?
            })
        })
        .catch(console.error);
    }

    _openPresentationChoosingDialog() {
        let fileInput = document.createElement("input");
        fileInput.type = "file";
        fileInput.accept = ".pptx";
        fileInput.click();

        fileInput.onchange = () => {
            let file = fileInput.files[0];
            this._uploadPresentationForChecking(file);
        };
    }

    render() {
        this._app = useContext(AppContext).app;

        return html`
            <div id="new-presentation-downloading-area"
                onclick=${() => this._openPresentationChoosingDialog()}
                ondrop=${event => {event.preventDefault(); this._uploadPresentationForChecking(event.dataTransfer.files[0])}}
                ondragover=${event => {event.preventDefault(); event.dataTransfer.dropEffect = "move";}}
            >Перетащи презентацию или кликни меня чтобы выбрать её</div>
            <${CheckingSettings} ref=${this._checkingSettingsRef} />
            <${ReportsList} />
        `;
    }
}