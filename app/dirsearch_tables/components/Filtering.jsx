import _ from 'lodash'
import React from 'react'

import { Button } from 'react-bootstrap'

import FilteringButtons from '../presentational/FilteringButtons.jsx'


class Filtering extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		var buttons = [];
		_.forOwn(this.props.filters, (value, key) => {
			buttons.push(<Button key={key} onClick={() => this.props.triggerFilter(key)}>{value.name}</Button>);
		});

		return (
			<div>{buttons}</div>
		)
	}
}

export default Filtering;