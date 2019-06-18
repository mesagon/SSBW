import React, { Component } from 'react'
import Peli from './Peli'

export default class Todas extends Component {


    constructor(props) {
        super(props)
        this.state = {                // variable estado de la clase, lista de películas
          pelis: [{title:'el bueno, el feo y el malo'}]
         }
      }

    // llamada al API
    componentDidMount() {
      fetch('https://localhost/miapp/api/pelis/?format=json')  // o el que sea
        .then(res => { return res.json()})
        .then(data => {
          console.log(data)
          this.setState({pelis:data})
        }).catch(error => {
          console.log(error)
        })

      }

      render() {
        // re-renderiza al cambiar el state
        return (
          <div>
            Todas las pelis: <br />
            {this.state.pelis.map(peli => {  // arrow function
              return (
                <Peli peli={peli} />
              )
            })
          }
          </div>
        )
      }
}
