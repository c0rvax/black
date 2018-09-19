import React from 'react'

import ScopesSocketioEventsEmitter from '../../redux/scopes/ScopesSocketioEventsEmitter.js'

import HostsTable from './HostsTable.jsx'

class HostsTableTracked extends React.Component {

	constructor(props) {
		super(props);

		this.scopesEmitter = new ScopesSocketioEventsEmitter();		

		this.deleteScope = this.deleteScope.bind(this);
	}

	deleteScope(scope_id) {
		this.props.triggerSetLoaded(false);
		this.scopesEmitter.requestDeleteScope(scope_id, this.props.project_uuid, "hostname");
	}

	render() {
		return (
			<HostsTable hosts={this.props.hosts}
						project_uuid={this.props.project_uuid}
						deleteScope={this.deleteScope}
						applyFilters={this.props.applyFilters}
						triggerSetLoaded={this.props.triggerSetLoaded}
						renewHosts={this.props.renewHosts}
						requestUpdateHost={this.props.requestUpdateHost} />
		)
	}

}


export default HostsTableTracked;
