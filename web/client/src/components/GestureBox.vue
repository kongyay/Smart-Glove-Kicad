<template>
  <v-container>
    <v-card>
      <v-card-title primary-title>
        <div class="headline">{{gesture.name}}</div>
        <v-spacer></v-spacer>
        <v-btn color='orange' @click='addPose'>+ Add Pose</v-btn>
        <v-btn color='green' @click='saveGesture'><v-icon>save</v-icon></v-btn>
        <v-btn color='red' @click='removeGesture'><v-icon>delete_forever</v-icon></v-btn>
      </v-card-title>

      <v-expansion-panel>
        <v-expansion-panel-content
          v-for="(pose,i) in poses"
          :key="i"
        >
          <div slot="header"><b>{{i}}). </b> {{ pose.name }}</div>
          <v-card>
            <v-layout>
              <v-flex xs5>
                <v-img
                  :src='pose.pic'
                  height="125px"
                  contain
                ></v-img>
              </v-flex>
              <v-flex xs7>
                <v-card-title primary-title>
                  <v-select v-if="getChoicePose.length>0"
                    :value="pose.name"
                    @change="editPose($event,i)"
                    :items="getChoicePose.map(c=>c.name)"
                    label="Pose"
                  ></v-select>
                </v-card-title>
              </v-flex>
            </v-layout>
            <v-divider light></v-divider>
            <v-card-actions class="pa-3" v-if="poses.length>1">
              <v-spacer></v-spacer>
              <v-btn color='red' flat  @click='removePose(i)'>Remove</v-btn>
            </v-card-actions>
          </v-card>

        </v-expansion-panel-content>
        <v-expansion-panel-content>
          <div slot="header">Action</div>
          <v-container>
            <v-layout column>

              <v-flex>
                <v-select v-if="getChoiceAction.length>0"
                  :items="getChoiceAction.map(c=>c.name)"
                  :value="action.name"
                  @change="editAction"
                  label="Action"
                  outline
                ></v-select>
              </v-flex>

              <v-flex>
                <v-layout wrap>
                  <v-flex xs12 v-if='action.name==="Display"'>
                    <v-textarea
                      label="Text"
                      v-model="gestureAction.args.text"
                    ></v-textarea>
                  </v-flex>
                  <v-flex xs12 v-else-if='action.name==="Http"'>
                    <v-select
                      label="Request Type"
                      v-model="gestureAction.args.type"
                      :items="['GET','POST']"
                      chips
                    ></v-select>
                    <v-text-field
                      label="URL"
                      v-model="gestureAction.args.url"
                    ></v-text-field>
                    <v-textarea
                      label="Parameters"
                      v-model="gestureAction.args.params"
                    ></v-textarea>
                  </v-flex>
                  <v-flex xs12 v-else-if='action.name==="Draw"'>
                    <v-textarea
                      label="Pixels"
                      v-model="gestureAction.args.pixels"
                    ></v-textarea>
                    <table>
                      <tr v-for="(v,i) in 64" :key="'r'+i">
                        <td v-for="(v,j) in 128" :key="'c'+j" :class="pixels === 1 ? 'white':'black'">.</td>
                      </tr>
                    </table>
                  </v-flex>
                </v-layout>
              </v-flex>

            </v-layout>
          </v-container>

        </v-expansion-panel-content>
      </v-expansion-panel>

    </v-card>
  </v-container>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
export default {
  props: {
    profile_name: String,
    gestureAction: Object
  },
  data () {
    return {
      isOpen: {}
    }
  },
  computed: {
    ...mapGetters(['getChoicePose', 'getChoiceAction', 'getChoiceGesture']),
    gesture () {
      return this.gestureAction.gesture
    },
    action () {
      return this.gestureAction.action
    },
    args () {
      return this.gestureAction.args
    },
    poses () {
      return this.gestureAction.gesture.poses
    },
    pixels () {
      return this.gestureAction.args.pixels || Array.from(Array(64), () => new Array(128).fill(0))
    }
  },
  methods: {
    ...mapMutations(['REMOVE_GESTURE']),
    goPose (name) {
      this.currentPose = name
    },
    editPose (name, i) {
      this.gestureAction.gesture.poses[i] = this.getChoicePose.find(c => c.name === name)
      this.$forceUpdate()
    },
    editAction (name) {
      this.gestureAction.action = this.getChoiceAction.find(c => c.name === name)
      this.$forceUpdate()
    },
    saveGesture () {
      console.log('Saving Gesture....')
      this.$socket.emit('saveGesture', this.profile_name, this.gestureAction)
    },
    removeGesture () {
      if (confirm(`Are you sure you want to remove "${this.gesture.name}"?`)) {
        this.REMOVE_GESTURE(this.gesture.name)
      } else {
        // Do nothing!
      }
    },
    addPose () {
      this.gestureAction.gesture.poses.push(this.getChoicePose[0])
    },
    removePose (i) {
      this.gestureAction.gesture.poses.splice(i, 1)
    }
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
