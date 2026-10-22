import AppKit
import Foundation
let jobs = try JSONSerialization.jsonObject(with: Data(contentsOf: URL(fileURLWithPath:CommandLine.arguments[1]))) as! [[String:Any]]
for job in jobs {
 try autoreleasepool {
  guard let image=NSImage(contentsOfFile:job["input"] as! String) else { fatalError("Cannot read SVG") }
  let w=job["width"] as! Int;let h=job["height"] as! Int
  guard let b=NSBitmapImageRep(bitmapDataPlanes:nil,pixelsWide:w,pixelsHigh:h,bitsPerSample:8,samplesPerPixel:4,hasAlpha:true,isPlanar:false,colorSpaceName:.deviceRGB,bytesPerRow:0,bitsPerPixel:0), let c=NSGraphicsContext(bitmapImageRep:b) else {fatalError("Cannot allocate bitmap")}
  NSGraphicsContext.saveGraphicsState();NSGraphicsContext.current=c;c.imageInterpolation = .high
  image.draw(in:NSRect(x:0,y:0,width:w,height:h),from:.zero,operation:.copy,fraction:1)
  c.flushGraphics();NSGraphicsContext.restoreGraphicsState()
  try b.representation(using:.png,properties:[:])!.write(to:URL(fileURLWithPath:job["output"] as! String))
 }
}
print("Rendered \(jobs.count) PNG exports")
