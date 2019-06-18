import React, { Component } from 'react'

export default class Peli extends Component {

	render() {

		var peli = this.props.peli;   // Props desde el componente de arriba.
		return(
		   <div key={peli.id}>
		      <h4>{peli.title}</h4>
		      <p><b>Plot:</b> {peli.plot}</p>
		      <p><b>Year:</b> {peli.year}.</p>
		      <p><b>Runtime:</b> {peli.runtime} min.</p>
		      <hr />
		   </div>
		  )
	}
}

