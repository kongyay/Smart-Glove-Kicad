<template>
  <div>
    <v-expansion-panel  expand>
      <v-expansion-panel-content>
        <div slot="header">Import...</div>
        <v-card>
          <v-card-text class="grey lighten-5">
            <div class="panel panel-sm">
                <div class="form-group">
                  <label for="csv_file" class="control-label col-sm-3 text-right">CSV file to import</label>
                  <div class="col-sm-9">
                    <input type="file" id="csv_file" name="csv_file" class="form-control" @change="loadCSV($event)">
                  </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
export default {
  data () {
    return {
      panelOpen: false,
      dataRead: {}
    }
  },
  computed: {
    ...mapGetters(['getHeadNames']),
    filteredHeader () {
      return [...this.getHeadNames.slice(9, 14), 'gesture']
    }
  },
  methods: {
    ...mapMutations(['IMPORT_CAPTURE']),
    loadCSV (e) {
      if (window.FileReader) {
        var reader = new FileReader()
        reader.readAsText(e.target.files[0])
        // Handle errors load
        reader.onload = (event) => {
          var csv = event.target.result
          csv = csv.split('\n').map(e => e.split(','))
          let lastname = ''
          csv.forEach(e => {
            let name = e[e.length - 1]
            e = e.slice(0, -1)
            e = e.map(x => parseInt(x))

            if (name in this.dataRead === false) {
              this.dataRead[name] = []
            } else {
              let cutname = lastname.split('.')[0]
              if (cutname !== name) {
                let i = 0
                let newname = name
                do {
                  newname = name + '.' + i++
                } while (newname in this.dataRead)
                name = newname
                this.dataRead[name] = []
              } else if (cutname === name) {
                name = lastname
              }
            }
            lastname = name

            if (e.length === 9) {
              e = [...e, 0, 0, 0, 0, 0]
            } else if (e.length === 5) {
              e = [0, 0, 0, 0, 0, 0, 0, 0, 0, ...e]
            }
            this.dataRead[name].push(e)
          })

          this.IMPORT_CAPTURE(this.dataRead)
          console.log(this.dataRead)
        }
        reader.onerror = (event) => {
          if (event.target.error.name === 'NotReadableError') {
            alert("Can't read file !")
          }
        }
      } else {
        alert('FileReader are not supported in this browser.')
      }
    }
  },
  components: {}
}
</script>
