import Foundation
import CoreText
import CoreGraphics
let inputURL = URL(fileURLWithPath: CommandLine.arguments[1])
let outputURL = URL(fileURLWithPath: CommandLine.arguments[2])
let jobs = try JSONSerialization.jsonObject(with: Data(contentsOf: inputURL)) as! [[String:Any]]
func n(_ v:CGFloat)->String { String(format:"%.3f",Double(v)).replacingOccurrences(of:#"\.?0+$"#,with:"",options:.regularExpression) }
func p(_ v:CGPoint)->String { "\(n(v.x)) \(n(v.y))" }
func svg(_ path:CGPath)->String {
 var r=""
 path.applyWithBlock { a in
  let e=a.pointee; let q=e.points
  switch e.type {
   case .moveToPoint:r += "M"+p(q[0])
   case .addLineToPoint:r += "L"+p(q[0])
   case .addQuadCurveToPoint:r += "Q"+p(q[0])+" "+p(q[1])
   case .addCurveToPoint:r += "C"+p(q[0])+" "+p(q[1])+" "+p(q[2])
   case .closeSubpath:r += "Z"
   @unknown default:fatalError("Unsupported path")
  }
 }
 return r
}
var results:[[String:Any]]=[]
for job in jobs {
 let font=CTFontCreateWithName((job["font"] as! String) as CFString, CGFloat(job["size"] as! Double),nil)
 guard (CTFontCopyPostScriptName(font) as String) == (job["font"] as! String) else { fatalError("Required local font unavailable") }
 let line=CTLineCreateWithAttributedString(NSAttributedString(string:job["text"] as! String,attributes:[NSAttributedString.Key(kCTFontAttributeName as String):font]))
 let path=CGMutablePath()
 for run in CTLineGetGlyphRuns(line) as! [CTRun] {
  let count=CTRunGetGlyphCount(run)
  var glyphs=[CGGlyph](repeating:0,count:count); var pos=[CGPoint](repeating:.zero,count:count)
  CTRunGetGlyphs(run,CFRange(location:0,length:0),&glyphs); CTRunGetPositions(run,CFRange(location:0,length:0),&pos)
  for i in 0..<count {
   if let shape=CTFontCreatePathForGlyph(font,glyphs[i],nil) {
    let t=CGAffineTransform(a:1,b:0,c:0,d:-1,tx:pos[i].x,ty:-pos[i].y)
    path.addPath(shape,transform:t)
   }
  }
 }
 let b=path.boundingBoxOfPath
 var t=CGAffineTransform(translationX:-b.minX,y:-b.minY)
 let shape=path.copy(using:&t)!
 results.append(["id":job["id"]!,"d":svg(shape),"width":b.width,"height":b.height])
}
try JSONSerialization.data(withJSONObject:results,options:[.sortedKeys]).write(to:outputURL)
print("Outlined \(results.count) text lines")
