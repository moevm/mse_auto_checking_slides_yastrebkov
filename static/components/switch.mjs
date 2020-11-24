import {Component, html} from "../preact.mjs";

export class Switch extends Component {
    constructor(props) {
        super(props);

        this.state = { index: -1 };
        this.switch();
    }


    switch() {
        const nextIndex = (this.state.index + 1) % this.props.valuesWithPrintable.length;
        this.setState({ index: nextIndex});
        if (this.props.onSwitch)
            this.props.onSwitch(this.props.valuesWithPrintable[nextIndex].value);
    }

    render() {
        return html`
            <div class="switch" onclick=${() => this.switch()}>
                ${
                    this.props.valuesWithPrintable.map(({printable}, index) => 
                        html`<div class=${index === this.state.index ? "switched" : ""}>${printable}</div>`
                    )
                }
            </div>
        `;
    }
}
