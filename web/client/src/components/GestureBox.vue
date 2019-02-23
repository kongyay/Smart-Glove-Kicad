<template>
  <div>
  <v-btn block outline :color="selected? 'primary':'blue-grey'" @click="isOpen=!isOpen">
      <v-icon left>{{ selected? 'check_box' : 'indeterminate_check_box' }}</v-icon>{{gesture.name}}
  </v-btn>
  <v-dialog v-model="isOpen" width="600px">
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
                    :items="getNoDupePose(i).map(c=>c.name)"
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

      </v-expansion-panel>

    </v-card>
  </v-dialog>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
export default {
  props: {
    gesture: Object,
    selected: Boolean
  },
  data () {
    return {
      isOpen: false
    }
  },
  computed: {
    ...mapGetters(['getChoicePose', 'getProfile', 'getProfileList']),
    poses () {
      return this.gesture.poses
    }
  },
  methods: {
    ...mapMutations(['REMOVE_GESTURE']),
    getNoDupePose (i) {
      return this.getChoicePose.filter(p => !(i > 0 && p.name === this.poses[i - 1].name) && !(i < this.poses.length - 1 && p.name === this.poses[i + 1].name))
    },
    editPose (name, i) {
      if (i > 0 && name === this.poses[i - 1].name) {
        alert(`Pose ${i} can't be the same as ${i - 1} (${name})`)
      } else if (i < this.poses.length - 1 && name === this.poses[i + 1].name) {
        alert(`Pose ${i} can't be the same as ${i + 1} (${name})`)
      } else {
        this.gesture.poses[i] = this.getChoicePose.find(c => c.name === name)
        this.saveGesture()
      }
      this.$forceUpdate()
    },
    saveGesture () {
      console.log('Saving Gesture....')
      this.$socket.emit('saveGesture', this.gesture)
    },
    removeGesture () {
      for (let p in this.getProfileList) {
        if (this.getProfile(p).gestures_actions.map(ga => ga.gesture.name).indexOf(this.gesture.name) > -1) {
          return alert('This gesture is being set by some Gesture->Action, Please remove them before deleting this gesture')
        }
      }
      if (confirm(`Are you sure you want to remove "${this.gesture.name}"?`)) {
        this.$socket.emit('removeGesture', this.gesture.name)
        this.REMOVE_GESTURE(this.gesture.name)
      } else {
        // Do nothing!
      }
    },
    addPose () {
      this.gesture.poses.push(this.getNoDupePose(this.poses.length)[0] || this.getChoicePose[0])
    },
    removePose (i) {
      this.gesture.poses.splice(i, 1)
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
