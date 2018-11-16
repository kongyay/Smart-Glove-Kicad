<template>
  <v-container>
    <v-card color="blue-grey darken-2" class="white--text">
      <v-card-title primary-title>
        <div class="headline">{{name}}</div>
      </v-card-title>

        <v-stepper v-model='currentStep'>
          <v-stepper-header>
            <template v-for="(step,i) in steps">
              <v-stepper-step
                :complete="i+1 === currentStep"
                :key="`${i+1}-step`"
                :step="i+1"
                editable
              >
                {{step.name}}
              </v-stepper-step>

              <v-divider
                v-if="i+1 !== steps.length"
                :key="i+1"
              ></v-divider>
            </template>
          </v-stepper-header>

          <v-stepper-items>
            <v-stepper-content
              v-for="(step,i) in steps"
              :key="`${i+1}-content`"
              :step="i+1"
            >

              <v-layout row align-center justify-center fill-height>
                <v-flex xs3 >
                  <img src='@/assets/left.png'/>
                </v-flex>
                <v-flex>
                  <v-layout column>
                  <v-select
                    :items="[step.pose]"
                    label="Pose"
                  ></v-select>
                  <v-select
                    :items="[step.movement]"
                    label="Movement"
                  ></v-select>
                  </v-layout>
                </v-flex>
                </v-layout>

              <v-btn
                color="primary"
                @click="editStep(step)"
              >
                Edit Step
              </v-btn>

              <v-btn color='red' flat>Remove</v-btn>

            </v-stepper-content>
          </v-stepper-items>
        </v-stepper>

      <v-card-actions>
        <v-btn flat dark>Edit Gesture</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>

export default {
  props: {
    name: String
  },
  data () {
    return {
      steps: [{name: 'Swipe Left', pose: 'Open', movement: 'Left'}, {name: 'Heart', pose: 'Miniheart', movement: 'Idle'}, {name: 'Step 3', pose: 'Miniheart', movement: 'Idle'}, {name: 'Step 4', pose: 'Miniheart', movement: 'Idle'}, {name: 'Step 5', pose: 'Miniheart', movement: 'Idle'}],
      currentStep: 1
    }
  },
  methods: {
    goStep (name) {
      this.currentStep = name
    },
    editStep (name) {
      console.log('Edit', name)
    }
  }
}
</script>

<style scoped>
img {
  width: 50px;
  height: 50px;
}
</style>
