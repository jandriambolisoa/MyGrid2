import { Colors } from '@/theme';
import { View, type ViewProps, StyleSheet } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

export function Container({ style, ...otherProps }: ViewProps) {

  const insets = useSafeAreaInsets();

  return (
    <View style={[
      styles.container,
      {
        paddingTop: insets.top,
        paddingBottom: insets.bottom,
        paddingLeft: insets.left,
        paddingRight: insets.right
      },
      style
    ]} {...otherProps}>
      {/* Your widget content goes here */}
    </View>
  );
}



const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.light.background
  }
})