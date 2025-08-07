import { StyleSheet, Text, type TextProps } from 'react-native';
import { Colors } from '@/constants/Colors';

export type MainTextProps = TextProps & {
  type?: 'light' | 'dark';
  bold?: boolean;
};

export function MainText({
  style,
  type = 'light',
  bold = false,
  ...rest
}: MainTextProps) {
  return (
    <Text
      style={[
        type === 'light' ? styles.light : undefined,
        type === 'dark' ? styles.dark : undefined,
        bold ? { fontFamily: 'AlteHaasGrotesk-Bold' } : { fontFamily: 'AlteHaasGrotesk' },
        style,
      ]}
      {...rest}
    />
  )
}

const styles = StyleSheet.create({
  light: {
    color: Colors.light.lightText,
    fontSize: 16
  },
  dark: {
    color: Colors.light.darkText,
    fontSize: 16
  }
})