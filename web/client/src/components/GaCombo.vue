<template>
  <div>
    <v-card style="margin: 10px">

      <v-card-text>
        <v-layout row>
          <v-flex xs6>
            <!-- <v-btn v-if="ga.gesture" block outline color="primary" class="item">{{ga.gesture.name}}</v-btn> -->
            <v-select
              :value="ga.gesture ? ga.gesture.name:''"
              :items="choiceGesture.map(c=>c.name)"
              @change="editGesture($event)"
              label="Define gesture"
              color="primary"
              background-color="primary"
              outline
            ></v-select>
            <!-- <v-btn v-else block outline color="grey" style="border-style: dashed">Add gesture</v-btn> -->
          </v-flex>

          <v-icon>arrow_right_alt</v-icon>

          <v-flex xs6>
            <!-- <v-btn v-if="ga.action" block outline color="pink" class="item">{{ga.action.name}}</v-btn> -->
            <v-select
              :value="ga.action ? ga.action.name:''"
              :items="choiceAction.map(c=>c.name)"
              @change="editAction($event)"
              label="Define action"
              color="primary"
              background-color="pink"
              outline
            ></v-select>
            <!-- <v-btn v-else block outline color="grey" style="border-style: dashed">Define action for this combo</v-btn> -->
          </v-flex>
        </v-layout>
        <v-layout>
        <v-expansion-panel v-model='argOpen' expand>
          <v-expansion-panel-content>
            <div slot="header">Args</div>
            <v-card>
              <v-card-text>
                    <v-flex xs12 v-if='ga.action.name==="Display"'>
                      <v-textarea
                        label="Text"
                        v-model="ga.args.text"
                        @change="save()"
                      ></v-textarea>
                    </v-flex>
                    <v-flex xs12 v-else-if='ga.action.name==="Http"'>
                      <v-select
                        label="Request Type"
                        v-model="ga.args.type"
                        :items="['GET','POST']"
                        @change="save()"
                        chips
                      ></v-select>
                      <v-text-field
                        label="URL"
                        v-model="ga.args.url"
                        @change="save()"
                      ></v-text-field>
                      <v-textarea
                        label="Parameters"
                        v-model="ga.args.params"
                        @change="save()"
                      ></v-textarea>
                    </v-flex>
                    <v-flex xs12 v-else-if='ga.action.name==="Draw"'>
                      <v-textarea
                        label="Pixels"
                        v-model="ga.args.pixels"
                        @change="save()"
                      ></v-textarea>
                      <table>
                        <tr v-for="(v,i) in 64" :key="'r'+i">
                          <td v-for="(v,j) in 128" :key="'c'+j" :class="pixels === 1 ? 'white':'black'">.</td>
                        </tr>
                      </table>
                    </v-flex>
                </v-card-text>

              <!-- <v-divider light></v-divider>
              <v-card-actions class="pa-3" >
                <v-spacer></v-spacer>
                <v-btn color='green' flat  @click='editArg()'>Save</v-btn>
              </v-card-actions> -->
            </v-card>

          </v-expansion-panel-content>
        </v-expansion-panel>
        </v-layout>
      </v-card-text>
      <v-card-text style="position: relative">
        <v-btn
          color="red"
          dark small absolute top right icon
          @click="remove"
        >
          <v-icon>close</v-icon>
        </v-btn>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { mapMutations } from 'vuex'
export default {
  props: {
    ga: Object,
    choiceGesture: Array,
    choiceAction: Array,
    profileName: String
  },
  data () {
    return {
      oldName: null,
      argOpen: []
    }
  },
  computed: {

  },
  methods: {
    ...mapMutations(['SET_GA', 'REMOVE_GA']),
    editGesture (name) {
      this.oldName = this.ga.gesture.name
      this.ga.gesture = this.choiceGesture.find(c => c.name === name)
      this.save()
    },
    editAction (name) {
      this.argOpen = [true]
      this.ga.action = this.choiceAction.find(c => c.name === name)
      this.save()
    },
    save () {
      console.log(this.profileName, this.oldName, this.ga)
      this.$socket.emit('saveGA', this.profileName, this.oldName, this.ga)
      this.SET_GA({'name': this.ga.gesture.name, 'newGA': this.ga})
      this.$forceUpdate()
    },
    remove () {
      if (confirm(`Are you sure you want to remove "${this.ga.gesture.name}->${this.ga.action.name}"?`)) {
        this.$socket.emit('removeGA', this.profileName, this.ga.gesture.name)
        this.REMOVE_GA(this.ga.gesture.name)
      } else {
        // Do nothing!
      }
    }
  },
  created () {
    this.oldName = this.ga.gesture.name
  },
  components: {

  }
}
</script>

<style scoped>
img {
  width: 50px;
  height: 50px;
}
table {
  width: 100%;
  table-layout: fixed;
  border-collapse: collapse;
}
table, th, td {
  border: 1px solid black;
}
.white {
  background-color: white;
}
.black {
  background-color: black;
}
</style>
