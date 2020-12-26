import {post} from "../ajax.mjs";
import {Component, html, useContext} from "../preact.mjs";
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

export class PresentationUploadingArea extends Component {
    constructor(props) {
        super(props);

        this.state = {};
    }

    _uploadPresentationForChecking(file) {
        if (!file)
            return;

        toBase64(file).then(presentation => {
            post("/api/check-presentation", {
                presentation,
                fileName: file.name,
                ...this.props.getSettings()
            }, {onProgress: progress => this.setState({progress})})
            .then(response => {
                if (!response || !response.success) {
                    this.setState({progress: -1})
                    return;
                }
                this._app.relocate('/report/' + response.reportId);
                this._app.fetchReports(); // TODO?
            })
        })
        .catch(error => console.error(error))
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
        this._app = useContext(AppContext);

        let message;
        let indicator = html`<div class="progress-indicator" style="width: ${this.state.progress * 100}%" />`;
        if (this.state.progress === undefined) {
            message = html`Перетащи презентацию или кликни меня чтобы выбрать её`;
            indicator = null;
        }
        else if (this.state.progress === 1)
            message = html`Обработка...`;
        else if (this.state.progress < 0) {
            message = html`Не поддерживается :(`;
            indicator = html`<div class="fail-indicator" />`;
        }
        else
            message = html`Загрузка...`;

        const userHandlers = ('progress' in this.state && this.state.progress !== -1) ? {} : {
            onclick: () => this._openPresentationChoosingDialog(),
            ondrop: event => {event.preventDefault(); this._uploadPresentationForChecking(event.dataTransfer.files[0])},
            ondragover: event => {event.preventDefault(); event.dataTransfer.dropEffect = "move";},
        };

        return html`
            <div id="new-presentation-uploading-area" ...${userHandlers}
            >
                ${message}
                ${indicator}
            </div>
        `
    }
}