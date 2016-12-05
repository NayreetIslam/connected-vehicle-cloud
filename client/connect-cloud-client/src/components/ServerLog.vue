<template>
  <textarea id="serverlog" cols="50" rows="5">{{ log }}</textarea>
</template>

<script>
export default {
  name: 'ServerLog',
  props: ['log']
}
</script>

<style>
#serverlog {

}
</style>
