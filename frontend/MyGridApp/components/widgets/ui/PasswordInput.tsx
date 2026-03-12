import { View, TouchableOpacity, TextInput, TextInputProps } from "react-native";
import { GlobalStyles, Colors } from "@/theme";
import { Octicons } from "@expo/vector-icons";

export function PasswordInput ({
  password='',
  showPass=false,
  setShowPass,
  ...otherProps
} : TextInputProps & {
  password: string;
  showPass?: boolean;
  setShowPass?: () => void;
}) {
  return (
    <View style={{ alignSelf: 'stretch' }}>
      <TextInput
        value={password}
        placeholderTextColor={Colors.light.disabledText}
        cursorColor={Colors.light.lightText}
        selectionColor={Colors.light.lightText}
        style={[GlobalStyles.button, GlobalStyles.loginButton]}
        secureTextEntry={showPass ? false : true}
        {...otherProps}
      />
      {password.length > 0 && <TouchableOpacity style={GlobalStyles.eye} onPress={setShowPass}>
        <Octicons name={showPass ? 'eye-closed' : 'eye'} size={20} color={Colors.light.lightText}/>
      </TouchableOpacity>}
    </View>
  )
}