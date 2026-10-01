import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Darsyar Widget Host")
                .font(.system(size: 28, weight: .bold, design: .rounded))
            Text("Add \"Darsyar Users\" from Desktop > Edit Widgets.")
                .foregroundStyle(.secondary)
                .font(.system(size: 14, weight: .regular, design: .rounded))
        }
        .padding(28)
        .frame(minWidth: 560, minHeight: 240)
    }
}
