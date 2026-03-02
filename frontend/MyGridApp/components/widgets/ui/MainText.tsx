import { StyleSheet, Text, type TextProps } from 'react-native';
import { Colors, Constants } from '@/theme';

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
        {
          textAlign: 'center'
        },
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
    fontSize: Constants.fontSizes.mainText
  },
  dark: {
    color: Colors.light.darkText,
    fontSize: Constants.fontSizes.mainText
  }
})