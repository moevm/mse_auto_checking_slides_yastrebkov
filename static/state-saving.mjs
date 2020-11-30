export function createStateSaver() {
    return {state: undefined};
}

export const stateSaving = Base => class extends Base {
    constructor() {
        super(...arguments);
    }

    restoreState() {
        if (this.props.stateSaver.state) {
            Object.assign(this.state, this.props.stateSaver.state);
            this.props.stateSaver.state = undefined;
            return true;
        }
        return false;
    }

    componentWillUnmount() {
        if (super.componentWillUnmount)
            super.componentWillUnmount();
        this.props.stateSaver.state = this.state;
    }
}