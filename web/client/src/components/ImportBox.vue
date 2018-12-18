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
                    <input type="file" id="csv_file" name="csv_file" class="form-control" @change="file = $event.target.files[0]">
                  </div>
                  <v-btn v-if='file' color="secondary" @click='loadCSV(false)'>Import</v-btn>
                  <v-btn v-if='file' color="secondary" @click='loadCSV(true)'>Import Split</v-btn>
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
      file: null,
      dataRead: {}
    }
  },
  computed: {
    ...mapGetters(['getHeadNames', 'getMaxVals', 'getQuantized']),
    filteredHeader () {
      return [...this.getHeadNames.slice(9, 14), 'gesture']
    }
  },
  methods: {
    ...mapMutations(['IMPORT_CAPTURE_IMU']),
    loadCSV (isSplit) {
      if (window.FileReader) {
        var reader = new FileReader()
        reader.readAsText(this.file)
        // Handle errors load
        reader.onload = (event) => {
          var csv = event.target.result
          csv = csv.split('\n').map(e => e.split(','))
          let lastname = ''
          csv.forEach(e => {
            let name = e[e.length - 1]
            e = e.slice(0, -1)
            e = e.map((x, i) => parseInt(x))

            if (name in this.dataRead === false) {
              this.dataRead[name] = []
            } else {
              // check if name exist before
              let cutname = lastname.split('.')[0]
              if (cutname !== name) {
                let i = 0
                let newname = name
                do {
                  newname = name + '.' + i++
                } while (newname in this.dataRead)
                name = newname
                this.dataRead[name] = []
              } else if (cutname === name) { // if name doesn't change...
                // and if last name is already full, change to new name
                if (isSplit && this.dataRead[lastname].length >= 20) {
                  let i = 0
                  let newname = name
                  do {
                    newname = name + '.' + i++
                  } while (newname in this.dataRead)
                  name = newname
                  this.dataRead[name] = []
                } else { // last name is not full, save to last name
                  name = lastname
                }
              }
            }
            lastname = name

            while (e.length < 18) {
              e.push(0)
            }

            this.dataRead[name].push([e.slice(0, 3), e.slice(3, 6), e.slice(6, 9), e.slice(9, 12), e.slice(12, 15), e.slice(15, 18)])
          })

          this.IMPORT_CAPTURE_IMU(this.dataRead)
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
