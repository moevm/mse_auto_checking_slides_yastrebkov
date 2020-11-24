import {createContext, Component, html} from '../preact.mjs';
import {Link} from "./link.mjs";
import {UserControls} from "./user-controls.mjs";
import {MainPageContent} from "./main-page-content.mjs";
import {SignInForm} from "./sign-in-form.mjs";
import {SignUpForm} from "./sign-up-form.mjs";
import {ReportView} from "./report-view.mjs";
import {get} from "../ajax.mjs";

export const AppContext = createContext(null);

export const studentDegreesWithPrintable = {
    'bachelor': 'Бакалавр',
    'master': 'Магистр',
};
export function studentDegreesWithPrintableArray() {
    return Object.entries(studentDegreesWithPrintable)
        .map(([value, printable]) => ({value, printable}));
}

export class App extends Component {
    constructor(props) {
        super(props);

        this.state = {
            location: window.location.pathname,
            login: localStorage.login,
            authToken: localStorage.authToken,
        }

        window.addEventListener("popstate", () => this.setState({location: window.location.pathname}));
    }

    isLoggedIn() {
        return localStorage.login;
    }
    rememberSignIn(login, authToken) {
        localStorage.login = login;
        localStorage.authToken = authToken;
        this.setState({login, authToken});
    }
    logOut() {
        delete localStorage.login;
        delete localStorage.authToken;
        this.setState({login: undefined, authToken: undefined, reports: undefined});
    }

    relocate(path) {
        window.history.pushState(path, '', path);
        this.setState({location: path});
    }

    fetchReports() {
        if (!this.isLoggedIn())
            return;
        get('/api/reports')
        .then(result => {
            if (!result || !result.success)
                return;
            this.setState({reports: result.reports});
        });
    }

    render() {
        let contentElement = null;
        let contentOnLocations = {
            '/sign-in': SignInForm,
            '/sign-up': SignUpForm,
            '/report/(?<reportId>[0-9a-zA-Z]+)': ReportView,
            '/': MainPageContent,
        }
        for (let location in contentOnLocations) {
            let locationMatch = this.state.location.match(location);
            if (locationMatch) {
                contentElement = html`<${contentOnLocations[location]} ...${locationMatch.groups} />`;
                break;
            }
        }

        return html`
            <${AppContext.Provider} value=${{app: this}}><!--TODO try to just pass 'this'-->
                <div id="header">
                    <${Link} id="logo" href="/">ETU presentation checker<//>
                    <${UserControls} userName=${this.state.login} />
                </div>
                <div id="content">${contentElement}</div>
            <//>
        `;
    }
}
