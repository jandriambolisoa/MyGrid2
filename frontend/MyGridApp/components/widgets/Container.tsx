import { View, type ViewProps } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { GlobalStyles } from '@/theme';

export function Container({ style, ...otherProps }: ViewProps) {

  const insets = useSafeAreaInsets();

  return (
    <View style={[
      GlobalStyles.container,
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