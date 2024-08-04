import { View, Text, StyleSheet } from "react-native";
import React from "react";

interface HeaderProps {
  title: string;
  subtitle: string;
}

const Header = ({ title, subtitle }: HeaderProps) => {
  return (
    <View style={{ paddingLeft: 5 }}>
      <Text style={{ fontFamily: "niv-b", fontSize: 30 }}>{title}</Text>
      <Text style={{ fontFamily: "niv-l", fontSize: 16 }}>{subtitle}</Text>
    </View>
  );
};

export default Header;

const styles = StyleSheet.create({});
