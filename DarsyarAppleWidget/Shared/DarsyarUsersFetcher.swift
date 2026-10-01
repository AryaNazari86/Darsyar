import Foundation

struct DarsyarUsersResult {
    let value: String
    let status: String
    let isHealthy: Bool
    let date: Date
}

enum DarsyarUsersFetcher {
    static func fetch() async -> DarsyarUsersResult {
        guard let url = URL(string: "https://api.darsyar.net/dashboard/") else {
            return .init(value: "--", status: "Bad URL", isHealthy: false, date: .now)
        }

        var request = URLRequest(url: url)
        request.timeoutInterval = 12
        request.cachePolicy = .reloadIgnoringLocalCacheData

        do {
            let (data, response) = try await URLSession.shared.data(for: request)
            guard let http = response as? HTTPURLResponse else {
                return .init(value: "--", status: "No HTTP", isHealthy: false, date: .now)
            }

            guard (200...299).contains(http.statusCode) else {
                return .init(value: "--", status: "HTTP \(http.statusCode)", isHealthy: false, date: .now)
            }

            guard let html = String(data: data, encoding: .utf8) else {
                return .init(value: "--", status: "Decode error", isHealthy: false, date: .now)
            }

            if let users = parseTotalUsers(from: html) {
                return .init(value: users, status: "Live", isHealthy: true, date: .now)
            }

            return .init(value: "--", status: "Parse error", isHealthy: false, date: .now)
        } catch {
            return .init(value: "--", status: "Offline", isHealthy: false, date: .now)
        }
    }

    private static func parseTotalUsers(from html: String) -> String? {
        let pattern = #"<p[^>]*>\s*تعداد\s*کل\s*کاربران\s*</p>\s*<h4[^>]*>\s*([^<]+?)\s*</h4>"#
        guard let regex = try? NSRegularExpression(pattern: pattern, options: [.dotMatchesLineSeparators]) else {
            return nil
        }

        let range = NSRange(html.startIndex..<html.endIndex, in: html)
        guard let match = regex.firstMatch(in: html, options: [], range: range),
              let valueRange = Range(match.range(at: 1), in: html) else {
            return nil
        }

        return html[valueRange].trimmingCharacters(in: .whitespacesAndNewlines)
    }
}
