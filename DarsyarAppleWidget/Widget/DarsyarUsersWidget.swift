import WidgetKit
import SwiftUI

struct DarsyarEntry: TimelineEntry {
    let date: Date
    let users: String
    let status: String
    let isHealthy: Bool
}

struct DarsyarProvider: TimelineProvider {
    func placeholder(in context: Context) -> DarsyarEntry {
        .init(date: .now, users: "2234", status: "Live", isHealthy: true)
    }

    func getSnapshot(in context: Context, completion: @escaping (DarsyarEntry) -> Void) {
        completion(.init(date: .now, users: "2234", status: "Live", isHealthy: true))
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<DarsyarEntry>) -> Void) {
        Task {
            let result = await DarsyarUsersFetcher.fetch()
            let entry = DarsyarEntry(date: result.date, users: result.value, status: result.status, isHealthy: result.isHealthy)
            let next = Calendar.current.date(byAdding: .minute, value: 1, to: .now) ?? .now.addingTimeInterval(60)
            completion(Timeline(entries: [entry], policy: .after(next)))
        }
    }
}

struct DarsyarUsersWidgetView: View {
    let entry: DarsyarProvider.Entry

    var body: some View {
        ZStack {
            // Darsyar logo palette: #2C353E -> #FF3D60
            LinearGradient(
                colors: [
                    Color(red: 44.0/255.0, green: 53.0/255.0, blue: 62.0/255.0),
                    Color(red: 255.0/255.0, green: 61.0/255.0, blue: 96.0/255.0)
                ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )

            RoundedRectangle(cornerRadius: 22, style: .continuous)
                .fill(.ultraThinMaterial.opacity(0.42))
                .overlay(
                    RoundedRectangle(cornerRadius: 22, style: .continuous)
                        .stroke(Color.white.opacity(0.26), lineWidth: 1)
                )
                .padding(3)

            VStack(alignment: .leading, spacing: 8) {
                HStack {
                    Text("Darsyar")
                        .font(.system(size: 11, weight: .semibold, design: .rounded))
                        .padding(.horizontal, 9)
                        .padding(.vertical, 4)
                        .background(.ultraThinMaterial, in: Capsule())
                    Spacer()
                    Circle()
                        .fill(entry.isHealthy ? Color.green : Color.red)
                        .frame(width: 9, height: 9)
                }

                Text("Total Users")
                    .font(.system(size: 13, weight: .medium, design: .rounded))
                    .foregroundStyle(.white.opacity(0.9))

                Text(entry.users)
                    .font(.system(size: 40, weight: .bold, design: .rounded))
                    .minimumScaleFactor(0.7)
                    .lineLimit(1)
                    .foregroundStyle(.white)

                Spacer(minLength: 0)

                HStack {
                    Text("api.darsyar.net")
                        .font(.system(size: 10, weight: .regular, design: .rounded))
                        .foregroundStyle(.white.opacity(0.78))
                    Spacer()
                    Text(entry.status)
                        .font(.system(size: 10, weight: .semibold, design: .rounded))
                        .foregroundStyle(.white.opacity(0.88))
                }
            }
            .padding(14)
        }
        .containerBackground(.clear, for: .widget)
    }
}

struct DarsyarUsersWidget: Widget {
    let kind = "DarsyarUsersWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: DarsyarProvider()) { entry in
            DarsyarUsersWidgetView(entry: entry)
        }
        .configurationDisplayName("Darsyar Users")
        .description("Shows total users from api.darsyar.net/dashboard")
        .supportedFamilies([.systemSmall, .systemMedium])
    }
}
